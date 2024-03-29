#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
sys.path.append(os.path.dirname(__file__))
import redj
from quikcy_controller import apps
apps.set_root_dir(os.path.dirname(__file__))
hrm_app = apps.get_app_by_name("hrm")
print(hrm_app)
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_spa.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
