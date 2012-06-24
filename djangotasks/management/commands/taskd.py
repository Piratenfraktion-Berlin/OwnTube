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

import sys, time, os, atexit
import logging
from signal import SIGTERM


from django.core.management.base import BaseCommand

from django.utils.daemonize import become_daemon

LOG_FORMAT = '%(asctime)s %(process)d:%(name)s %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S %Z'

def _log_file():
    from django.conf import settings
    if hasattr(settings, 'TASKS_LOG_FILE'):
        return settings.TASKS_LOG_FILE
    else:
        return '/tmp/django-tasks.log'



#
# This class is inspired by http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ ,
# which was been put in the public domain by its author, Sander Marechal (http://www.jejik.com),
# see http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/#c6
# 
#

class Daemon:
    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        sys.stdout.flush()
        sys.stderr.flush()
        # TODO: give feedback to the user, on whether the daemon was started successfully,
        # i.e. verify that the daemon was started correctly.
        # This needs to be done in the *parent* process:
        # it  probably requires patching become_daemon, since we would have 
        # to add some processing *before* the sys.exit() for the parent.
        # This processing (a callback function ?) would likely wait for a few seconds while checking for the creation of the pidfile,
        # then wait another few seconds that the pid actually continues existing: if it doesn't continue existing, 
        # it would simply print an error.       
        become_daemon()

        atexit.register(self._delpid)
        self._setpid()

    def _delpid(self):
        try:
            os.remove(self.pidfile)
        except:
            pass

    def _setpid(self):
        file(self.pidfile,'w+').write("%d\n" % os.getpid())
        
    def _getpid(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        return pid

    def start(self):
        pid = self._getpid()
        if pid:
            try:
                os.getsid(pid)
                sys.stderr.write("Daemon already running.\n")
            except:
                sys.stderr.write("pidfile %s already exists, but daemon is not running. Delete pidfile and retry.\n" % self.pidfile)
            sys.exit(1)
    
        self.daemonize()
        self.run()

    def stop(self):
        pid = self._getpid()
        if not pid:
            sys.stderr.write("pidfile %s does not exist, cannot stop daemon.\n" % self.pidfile)
            return # not an error in a restart

        # TODO: maybe give feedback to the user, on whether the daemon was stopped successfully ?
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        pass

class TaskDaemon(Daemon):
    def run(self):
        from djangotasks.models import Task
        for handler in list(logging.getLogger().handlers):
            logging.getLogger().removeHandler(handler)

        if _log_file():
            logging.basicConfig(level=logging.INFO,
                                format=LOG_FORMAT,
                                datefmt=LOG_DATEFMT,
                                filename=_log_file())
        else:
            logging.basicConfig(level=logging.INFO)

        Task.objects.scheduler()

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) == 1 and args[0] in ['start', 'stop', 'restart', 'run']:

            if args[0] in ['start', 'restart']:
                if _log_file():
                    print "Logging to %s" % _log_file()
            elif args[0] == 'run':
                # when running, force logging to console only
                from django.conf import settings
                settings.TASKS_LOG_FILE = ''
                
            daemon = TaskDaemon(os.path.join(os.getenv('TEMP') if (os.name == 'nt') else '/tmp',
                                             'django-taskd.pid'))
            getattr(daemon, args[0])()
        else:
            return "Usage: %s %s start|stop|restart|run\n" % (sys.argv[0], sys.argv[1])
