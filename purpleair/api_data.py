"""
Constants for PurpleAir API
"""
from datetime import timedelta
from sqlite3 import OperationalError

import requests_cache

# Set up cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=1))
try:
    requests_cache.core.remove_expired_responses()
except OperationalError:
    requests_cache.core.uninstall_cache()
    print('Unable to open cache or purge cache database, requests will not be cached!!!')


API_ROOT = 'https://www.purpleair.com/json'

PARENT_PRIMARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': 'PM1.0_CF_ATM_ug/m3',
    'field2': 'PM2.5_CF_ATM_ug/m3',
    'field3': 'PM10.0_CF_ATM_ug/m3',
    'field4': 'UptimeMinutes',
    'field5': 'ADC',
    'field6': 'Temperature_F',
    'field7': 'Humidity_%',
    'field8': 'PM2.5_CF_1_ug/m3',
}

PARENT_SECONDARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': '0.3um/dl',
    'field2': '0.5um/dl',
    'field3': '1.0um/dl',
    'field4': '2.5um/dl',
    'field5': '5.0um/dl',
    'field6': '10.0um/dl',
    'field7': 'PM1.0_CF_1_ug/m3',
    'field8': 'PM10.0_CF_1_ug/m3',
}

CHILD_PRIMARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': 'PM1.0_CF_ATM_ug/m3',
    'field2': 'PM2.5_CF_ATM_ug/m3',
    'field3': 'PM10.0_CF_ATM_ug/m3',
    'field4': 'UptimeMinutes',
    'field5': 'RSSI_dbm',
    'field6': 'Pressure_hpa',
    'field7': 'Blank',
    'field8': 'PM2.5_CF_1_ug/m3',
}

CHILD_SECONDARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': '0.3um/dl',
    'field2': '0.5um/dl',
    'field3': '1.0um/dl',
    'field4': '2.5um/dl',
    'field5': '5.0um/dl',
    'field6': '10.0um/dl',
    'field7': 'PM1.0_CF_1_ug/m3',
    'field8': 'PM10.0_CF_1_ug/m3'
}
