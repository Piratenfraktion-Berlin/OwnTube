#!/usr/bin/env python
import os
import sys

import site
import owntube.settings as settings

if settings.VIRTUALENV:
    site.addsitedir(settings.VIRTUALENV)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "owntube.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
