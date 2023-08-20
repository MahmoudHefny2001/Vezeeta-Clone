# example_project/settings/__init__.py

import os

# Determine the environment ('develpment' or 'production')
env = os.environ.get('DJANGO_ENV', 'development')

# Import the appropriate settings module based on the environment
if env == 'production':
    from .production_settings import *
else:
    from .development_settings import *