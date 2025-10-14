"""
WSGI config for clean_agri_shop project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_agri_shop.settings')

application = get_wsgi_application()
