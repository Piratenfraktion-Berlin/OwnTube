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
import sys
import logging

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = "task_id"
    
    def handle(self, *args, **options):
        if len(args) != 1:
            self.print_help(sys.argv[0], sys.argv[1])
            return
            
        if 'DJANGOTASKS_TESTING' in os.environ:
            # In tests, we make sure that we are using the right database connection
            # This code is heavily inspired by BaseDatabaseCreation._create_test_db in django/db/backends/creation.py
            # (why doesn't Django provides this as a public method ??)
            from django.db import connections
            for alias in connections:
                connection = connections[alias]
                connection.close()
                if connection.settings_dict['TEST_NAME']:
                    test_database_name = connection.settings_dict['TEST_NAME']
                else:
                    from django.db.backends.creation import TEST_DATABASE_PREFIX
                    test_database_name = TEST_DATABASE_PREFIX + connection.settings_dict['NAME']
                    
                connection.settings_dict["NAME"] = test_database_name
                if hasattr(connection.creation, '_rollback_works'):
                    # needed in Django 1.2, but not anymore in 1.3
                    can_rollback = connection.creation._rollback_works()
                    connection.settings_dict["SUPPORTS_TRANSACTIONS"] = can_rollback

            # Also register the test model
            from djangotasks import tests

        from djangotasks.models import Task, LOG
        # Ensure that task log messages will be sent to the standard output
        # thus caught in the task's log
        LOG.addHandler(logging.StreamHandler())
        LOG.setLevel(logging.INFO)

        return Task.objects.exec_task(*args)
        
