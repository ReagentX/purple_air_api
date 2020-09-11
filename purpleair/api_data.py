"""
Constants for PurpleAir API
"""
from datetime import timedelta
from sqlite3 import OperationalError

import requests_cache

# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=1))
try:
    requests_cache.core.remove_expired_responses()
except OperationalError:
    requests_cache.core.uninstall_cache()
    print('Unable to open cache or purge cache database, requests will not be cached!!!')


API_ROOT = 'https://www.purpleair.com/json'
