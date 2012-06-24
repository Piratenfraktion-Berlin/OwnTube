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


#
# Public API to use DjangoTasks.
#
# The functions below should be sufficient to work with djangotasks.
# Please enter bugs on http://code.google.com/p/django-tasks if you need anything more.
# This API is still work-in-progress: it may still change, although it is probably quite stable.
# 
#


# The Task model is public, to load tasks and read their status, log, pid, timings...
from djangotasks.models import Task


def register_task(method, documentation, *required_methods):
    ''' Register a method of a model class as a task that can be executed asynchronously

    The method must be an unbound method of a model class.
    '''
    Task.objects.register_task(method, documentation, *required_methods)


def tasks_for_object(object):
    ''' Return all the tasks that are registered for this model object.

    The returned tasks can then be used for display information... or to be started.
    '''
    return Task.objects.tasks_for_object(object.__class__, object.pk)


def task_for_object(object_method):
    ''' Return the task for this object method.

    The parameter must be the method of a bound object, not an unbound class method.
    This is a shortcut to calling tasks_for_object and selecting the task for the method
    '''
    return Task.objects.task_for_object(object_method.im_class, object_method.im_self.pk, object_method.im_func.__name__)


def task_for_function(function):
    ''' Create (or find, if has been created already) a task for this function. 

    Any package-level function that does not take any parameters can be run as a asynchronously. 
    
    Contrary to model objects methods, functions do not need to be registered in order to be available as tasks.'''
    return Task.objects.task_for_function(function)


def run_task(task):
    ''' Runs the task. 
    
    The task will be re-run (and the previous one archived) if it has already run. 
    In that case, the object returned by run_task will be the new task.'''
    return Task.objects.run_task(task.pk)


def cancel_task(task):
    '''Cancels the task.

    '''
    return Task.objects.cancel_task(task.pk)


def current_task():
    ''' In the proces that's executing a task, the task being executed. None in all other cases.'''
    return Task.objects.current_task
