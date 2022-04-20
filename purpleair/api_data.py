"""
Constants for PurpleAir API
"""


API_ROOT = 'https://www.purpleair.com/json'
THINGSPEAK_API_URL = "https://thingspeak.com/channels/{channel}/feed.csv?"

PARENT_PRIMARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': 'PM1.0 (CF=1) ug/m3',
    'field2': 'PM2.5 (CF=1) ug/m3',
    'field3': 'PM10.0 (CF=1) ug/m3',
    'field4': 'UptimeMinutes',
    'field5': 'ADC',
    'field6': 'Temperature_F',
    'field7': 'Humidity_%',
    'field8': 'PM2.5 (CF=ATM) ug/m3',
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
    'field7': 'PM1.0 (CF=ATM) ug/m3',
    'field8': 'PM10 (CF=ATM) ug/m3',
}

CHILD_PRIMARY_COLS = {
    'created_at': 'created_at',
    'entry_id': 'entry_id',
    'field1': 'PM1.0 (CF=1) ug/m3',
    'field2': 'PM2.5 (CF=1) ug/m3',
    'field3': 'PM10.0 (CF=1) ug/m3',
    'field4': 'UptimeMinutes',
    'field5': 'RSSI_dbm',
    'field6': 'Atmospheric Pressure',
    'field7': 'gas_sensor',
    'field8': 'PM2.5 (CF=ATM) ug/m3',
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
    'field7': 'PM1.0 (CF=ATM) ug/m3',
    'field8': 'PM10 (CF=ATM) ug/m3'
}
