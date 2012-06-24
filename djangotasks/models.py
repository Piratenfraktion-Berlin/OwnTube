#
# Copyright (c) 2010 by nexB, Inc. http://www.nexb.com/ - All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#    
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
# 
#     3. Neither the names of Django, nexB, Django-tasks nor the names of the contributors may be used
#        to endorse or promote products derived from this software without
#        specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
import sys
import time
import subprocess
import logging

from django.db import models
from django.conf import settings
from datetime import datetime
from os.path import join, exists, dirname, abspath
from collections import defaultdict
from django.db import transaction, connection
from django.utils.encoding import smart_unicode

from djangotasks import signals

LOG = logging.getLogger("djangotasks")

def _get_model_name(model_class):
    return smart_unicode(model_class._meta)

def _get_model_class(model_name):
    model = models.get_model(*model_name.split("."))
    if model == None:
        raise Exception("%s is not a registered model, cannot use this task" % model_name)
    return model


class TaskManager(models.Manager):
    '''The TaskManager class is not for public use. 


    The package-level API should be sufficient to use django-tasks.
    '''


    # The only real role of DEFINED_TASKS, in fact, is to keep track of the *current* list of dependent tasks for each task.
    # If we were to accept the fact that, when upgrading application code and changing the dependencies of tasks,
    # it is acceptable that the tasks that already exist in the DB will still use the "old" set of dependencies,
    # then we could store the list of dependencies as a field in the Task object, 
    # and DEFINED_TASKS wouldn't be needed anymore. I'm still hesitating a little between the two solutions.
    DEFINED_TASKS = defaultdict(list)

    # When executing a task, the current task being executed. 
    # Since only one task is executed per process, this can be a static.
    current_task = None

    def register_task(self, method, documentation, *required_methods):
        import inspect
        if not inspect.ismethod(method):
            raise Exception(repr(method) + " is not a class method")
        model = _get_model_name(method.im_class)
        if len(required_methods) == 1 and required_methods[0].__class__ in [list, tuple]:
            required_methods = required_methods[0]

        for required_method in required_methods:
            if not inspect.ismethod(required_method):
                raise Exception(repr(required_method) + " is not a class method")
            if required_method.im_func.__name__ not in [method_name for method_name, _, _ in TaskManager.DEFINED_TASKS[model]]:
                raise Exception(repr(required_method) + " is not registered as a task method for model " + model)
            
        TaskManager.DEFINED_TASKS[model].append((method.im_func.__name__, 
                                                 documentation if documentation else '',
                                                 ','.join(required_method.im_func.__name__ 
                                                          for required_method in required_methods)))

    def task_for_object(self, the_class, object_id, method, status_in=None):
        model = _get_model_name(the_class)
        if method not in [m for m, _, _ in TaskManager.DEFINED_TASKS[model]]:
            raise Exception("Method '%s' not registered for model '%s'" % (method, model))

        taskdef = [taskdef for taskdef in TaskManager.DEFINED_TASKS[model] 
                   if taskdef[0] == method][0]

        if not status_in:
            status_in = dict(STATUS_TABLE).keys()
            
        from django.core.exceptions import MultipleObjectsReturned
        try:
            task, created = self.get_or_create(model=model, 
                                               method=method,
                                               object_id=str(object_id),
                                               status__in=status_in,
                                               archived=False)
        except MultipleObjectsReturned, e:
            LOG.exception("Integrity error: multiple non-archived tasks, should not occur. Attempting recovery by archiving all tasks for this object and method, and recreating them")
            objects = self.filter(model=model, 
                                  method=method,
                                  object_id=str(object_id),
                                  status__in=status_in,
                                  archived=False).update(archived=True)
            task, created = self.get_or_create(model=model, 
                                               method=method,
                                               object_id=str(object_id),
                                               status__in=status_in,
                                               archived=False)

        if created:
            self.filter(pk=task.pk).update(description=taskdef[1])

        LOG.debug("Created task %d on model=%s, method=%s, object_id=%s", task.id, model, method, object_id)
        return self.get(pk=task.pk)

    def tasks_for_object(self, the_class, object_id):
        model = _get_model_name(the_class)

        return [self.task_for_object(the_class, object_id, method)
                for method, _, _ in TaskManager.DEFINED_TASKS[model]]
            
    def task_for_function(self, function):
        function_name = _to_function_name(function)
        function_task = FunctionTask.objects.get_or_create(function_name=function_name)
        return self.task_for_object(FunctionTask, function_name,
                                    FunctionTask.run_function_task.func_name)

    def run_task(self, pk):
        task = self.get(pk=pk)
        self._run_required_tasks(task)
        if task.status in ["scheduled", "running"]:
            return task
        if task.status in ["requested_cancel"]:        
            raise Exception("Task currently being cancelled, cannot run again")
        if task.status in ["cancelled", "successful", "unsuccessful"]:
            task = self._create_task(task.model, 
                                     task.method, 
                                     task.object_id)
            
        self.filter(pk=task.pk).update(status="scheduled")
        return self.get(pk=task.pk)

    def _run_required_tasks(self, task):
        for required_task in task.get_required_tasks():
            self._run_required_tasks(required_task)

            if required_task.status in ['scheduled', 'successful', 'running']:
                continue
            
            if required_task.status == 'requested_cancel':
                raise Exception("Required task being cancelled, please try again")

            if required_task.status in ['cancelled', 'unsuccessful']:
                # re-run it
                required_task = self._create_task(required_task.model, 
                                                  required_task.method, 
                                                  required_task.object_id)

            required_task.status = "scheduled"
            required_task.save()
            
    def cancel_task(self, pk):
        task = self.get(pk=pk)
        if task.status not in ["scheduled", "running"]:
            raise Exception("Cannot cancel task that has not been scheduled or is not running")

        # If the task is still scheduled, mark it requested for cancellation also:
        # if it is currently starting, that's OK, it'll stay marked as "requested_cancel" in mark_start
        self._set_status(pk, "requested_cancel", ["scheduled", "running"])


    # The methods below are for internal use on the server. Don't use them directly.
    def _create_task(self, model, method, object_id):
        return Task.objects.task_for_object(_get_model_class(model), object_id, method, 
                                            ["defined", "scheduled", "running", "requested_cancel"])

    def append_log(self, pk, log):
        if log:
            # not possible to make it completely atomic in Django, it seems
            rowcount = self.filter(pk=pk).update(log=(self.get(pk=pk).log + log))
            if rowcount == 0:
                raise Exception(("Failed to save log for task %d, task does not exist; log was:\n" % pk) + log)

    def mark_start(self, pk, pid):
        # Set the start information in all cases: That way, if it has been set
        # to "requested_cancel" already, it will be cancelled at the next loop of the scheduler
        rowcount = self.filter(pk=pk).update(pid=pid, start_date=datetime.now())
        if rowcount == 0:
            raise Exception("Failed to mark task with ID %d as started, task does not exist" % pk)

    def _set_status(self, pk, new_status, existing_status):
        if isinstance(existing_status, str):
            existing_status = [ existing_status ]
            
        if existing_status:
            rowcount = self.filter(pk=pk).filter(status__in=existing_status).update(status=new_status)
        else:
            rowcount = self.filter(pk=pk).update(status=new_status)
        if rowcount == 0:
            LOG.warning('Failed to change status from %s to "%s" for task %s',
                        "or".join('"' + status + '"' for status in existing_status) if existing_status else '(any)',
                        new_status, pk)

        return rowcount != 0

    def mark_finished(self, pk, new_status, existing_status):
        rowcount = self.filter(pk=pk).filter(status=existing_status).update(status=new_status, end_date=datetime.now())
        if rowcount == 0:
            LOG.warning('Failed to mark tasked as finished, from status "%s" to "%s" for task %s. May have been finished in a different thread already.',
                        existing_status, new_status, pk)
        else:
            LOG.info('Task %s finished with status "%s"', pk, new_status)
            # Sending a task completion Signal including the task and the object
            task = self.get(pk=pk)
            object = _get_model_class(task.model).objects.get(pk=task.object_id)
            signals.task_completed.send(sender=self, task=task, object=object)
    
    # This is for use in the scheduler only. Don't use it directly.
    def exec_task(self, task_id):
        if self.current_task:
            raise Exception("Task already running running in process")
        try:
            self.current_task = self.get(pk=task_id)

            the_class = _get_model_class(self.current_task.model)
            object = the_class.objects.get(pk=self.current_task.object_id)
            the_method =  getattr(object, self.current_task.method)

            the_method()
        finally:
            import sys
            sys.stdout.flush()
            sys.stderr.flush()
    
    # This is for use in the scheduler only. Don't use it directly
    def scheduler(self):
        # Run once to ensure exiting if something is wrong
        try:
            self._do_schedule()
        except:
            LOG.fatal("Failed to start scheduler due to exception", exc_info=1)
            return

        LOG.info("Scheduler started")
        while True:
            # Loop time must be enough to let the threads that may have be started call mark_start
            time.sleep(5)
            try:
                self._do_schedule()
            except:
                LOG.exception("Scheduler exception")

    def _do_schedule(self):
        # First cancel any task that needs to be cancelled...
        tasks = self.filter(status="requested_cancel",
                            archived=False)
        for task in tasks:
            LOG.info("Cancelling task %d...", task.pk)
            task._do_cancel()
            LOG.info("...Task %d cancelled.", task.pk)

        # ... Then start any new task
        tasks = self.filter(status="scheduled",
                            archived=False)
        for task in tasks:
            # only run if all the required tasks have been successful
            if any(required_task.status == "unsuccessful"
                   for required_task in task.get_required_tasks()):
                task.status = "unsuccessful"
                task.save()
                continue

            if all(required_task.status == "successful"
                   for required_task in task.get_required_tasks()):
                LOG.info("Starting task %s...", task.pk)
                task.do_run()
                LOG.info("...Task %s started.", task.pk)
                # only start one task at a time
                break

STATUS_TABLE = [('defined', 'ready to run'),
                ('scheduled', 'scheduled'),
                ('running', 'in progress',),
                ('requested_cancel', 'cancellation requested'),
                ('cancelled', 'cancelled'),
                ('successful', 'finished successfully'),
                ('unsuccessful', 'failed'),
                ]

          
class Task(models.Model):

    model = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    
    object_id = models.CharField(max_length=200)
    pid = models.IntegerField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=200,
                              default="defined",
                              choices=STATUS_TABLE,
                              )
    description = models.CharField(max_length=100, default='', null=True, blank=True)
    log = models.TextField(default='', null=True, blank=True)

    archived = models.BooleanField(default=False) # for history

    def __unicode__(self):
        return u'%s - %s.%s.%s' % (self.id, self.model.split('.')[-1], self.object_id, self.method)

    def status_string(self):
        return dict(STATUS_TABLE)[self.status]

    def status_for_display(self):
        return '<span class="%s">%s</span>' % (self.status, self.status_string())

    status_for_display.allow_tags = True
    status_for_display.admin_order_field = 'status'
    status_for_display.short_description = 'Status'

    def complete_log(self, directly_required_only=False):
        return '\n'.join([required_task.formatted_log() 
                          for required_task in self._unique_required_tasks(directly_required_only)])

    def get_required_tasks(self):
        taskdef = self._get_task_definition()
        return [Task.objects.task_for_object(_get_model_class(self.model), self.object_id, method)
                for method in taskdef[2].split(',') if method] if taskdef else []
    
    def can_run(self):
        return self.status not in ["scheduled", "running", "requested_cancel", ] #"successful"

    def formatted_log(self):
        from django.utils.dateformat import format
        FORMAT = "N j, Y \\a\\t P T"
        if self.status in ['cancelled', 'successful', 'unsuccessful']:
            return (self.description + ' started' + ((' on ' + format(self.start_date, FORMAT)) if self.start_date else '') +
                    (("\n" + self.log) if self.log else "") + "\n" +
                    self.description + ' ' + self.status_string() + ((' on ' + format(self.end_date, FORMAT)) if self.end_date else '') +
                    (' (%s)' % self.duration if self.duration else ''))
        elif self.status in ['running', 'requested_cancel']:
            return (self.description + ' started' + ((' on ' + format(self.start_date, FORMAT)) if self.start_date else '') +
                    (("\n" + self.log) if self.log else "") + "\n" +
                    self.description + ' ' + self.status_string())
        else:
            return self.description + ' ' +  self.status_string()
                    
    # Only for use by the manager: do not call directly, except in tests
    def do_run(self):
        if self.status != "scheduled":
            raise Exception("Task not scheduled, cannot run again")

        def exec_thread():
            returncode = -1
            try:
                # Do not start if it's not marked as scheduled
                # This ensures that we can have multiple schedulers
                if not Task.objects._set_status(self.pk, "running", "scheduled"):
                    return
                # execute the managemen utility, with the same python path as the current process
                env = dict(os.environ)
                env['PYTHONPATH'] = os.pathsep.join(sys.path)
                proc = subprocess.Popen([sys.executable, 
                                         '-c',
                                         'from django.core.management import ManagementUtility; ManagementUtility().execute()',
                                         'runtask', 
                                         str(self.pk),
                                         ],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        close_fds=(os.name != 'nt'), 
                                        env=env)
                Task.objects.mark_start(self.pk, proc.pid)
                buf = ''
                t = time.time()
                while proc.poll() is None:
                    line = proc.stdout.readline()
                    buf += line

                    if (time.time() - t > 1): # Save the log once every second max
                        Task.objects.append_log(self.pk, buf)
                        buf = ''
                        t = time.time()
                Task.objects.append_log(self.pk, buf)
                
                # Need to continue reading for a while: sometimes we miss some output
                buf = ''
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    buf += line
                Task.objects.append_log(self.pk, buf)

                returncode = proc.returncode

            except Exception, e:
                LOG.exception("Exception in calling thread for task %s", self.pk)
                import traceback
                stack = traceback.format_exc()
                try:
                    Task.objects.append_log(self.pk, "Exception in calling thread: " + str(e) + "\n" + stack)
                except Exception, ee:
                    LOG.exception("Second exception while trying to save the first exception to the log for task %s!", self.pk)

            Task.objects.mark_finished(self.pk,
                                       "successful" if returncode == 0 else "unsuccessful",
                                       "running")
            
        import thread
        thread.start_new_thread(exec_thread, ())

    def _do_cancel(self):
        if self.status != "requested_cancel":
            raise Exception("Cannot cancel task if not requested")

        try:
            if not self.pid:
                # This can happen if the task was only scheduled when it was cancelled.
                # There could be risk that the task starts *while* we are cancelling it, 
                # and we will mark it as cancelled, but in fact the process will not have been killed/
                # However, it won't happen because (in the scheduler loop) we *wait* after starting tasks, 
                # and before cancelling them. So no need it'll happen synchronously.
                return
                
            import signal
            os.kill(self.pid, signal.SIGTERM)
        except OSError, e:
            # could happen if the process *just finished*. Fail cleanly
            raise Exception('Failed to cancel task model=%s, method=%s, object=%s: %s' % (self.model, self.method, self.object_id, str(e)))
        finally:
            Task.objects.mark_finished(self.pk, "cancelled", "requested_cancel")

    def _unique_required_tasks(self, directly_required_only=False):
        unique_required_tasks = []
        for required_task in self.get_required_tasks():
            if directly_required_only:
                if required_task not in unique_required_tasks:
                    unique_required_tasks.append(required_task)
            else:
                for unique_required_task in required_task._unique_required_tasks():
                    if unique_required_task not in unique_required_tasks:
                        unique_required_tasks.append(unique_required_task)
        if self not in unique_required_tasks:
            unique_required_tasks.append(self)
        return unique_required_tasks

    def save(self, *args, **kwargs):
        if not self.pk:
            self._find_method() # will raise an exception if the method of this task is not registered
            
            # time to archive the old ones
            Task.objects.filter(model=self.model, 
                                method=self.method,
                                object_id=self.object_id,
                                archived=False).update(archived=True)

        super(Task, self).save(*args, **kwargs)

    def _get_task_definition(self):
        if self.model not in TaskManager.DEFINED_TASKS:
            LOG.warning("A task on model=%s exists in the database, but is not defined in the code", self.model)
            return None
        taskdefs = [taskdef for taskdef in TaskManager.DEFINED_TASKS[self.model] if taskdef[0] == self.method]
        if len(taskdefs) == 0:
            LOG.debug("A task on model=%s and method=%s exists in the database, but is not defined in the code", self.model, self.method)
            return None
        return taskdefs[0]

    def _find_method(self):
        the_class = _get_model_class(self.model)
        object = the_class.objects.get(pk=self.object_id)
        return getattr(object, self.method)

    def _compute_duration(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            min, sec = divmod((delta.days * 86400) + delta.seconds, 60)
            hour, min = divmod(min, 60)
            str = ((hour, 'hour'), (min, 'minute'), (sec, 'second'))
            return ', '.join(['%d %s%s' % (x[0], x[1],'s' if x[0] > 1 else '')
                              for x in str if (x[0] > 0)])

    duration = property(_compute_duration)
            
    objects = TaskManager()

def _to_function_name(function):
    import inspect
    if not inspect.isfunction(function):
        raise Exception(repr(function) + " is not a function")
    return function.__module__ + '.' + function.__name__


def _to_function(function_name):
    module_segments = function_name.split('.')
    module = __import__('.'.join(module_segments[:-1]))
    for segment in module_segments[1:]:
        module = getattr(module, segment)
    return module


class FunctionTask(models.Model):
    function_name = models.CharField(max_length=255,
                                     primary_key=True)
    def run_function_task(self):
        function = _to_function(self.function_name)
        return function()

Task.objects.register_task(FunctionTask.run_function_task, "Run a function task")


if 'DJANGOTASK_DAEMON_THREAD' in dir(settings) and settings.DJANGOTASK_DAEMON_THREAD:
    import logging
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(logging.INFO)

    import thread
    thread.start_new_thread(Task.objects.scheduler, ())
