"""
ASGI config for clean_agri_shop project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_agri_shop.settings')

application = get_asgi_application()
