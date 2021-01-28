#!python
""" Example program using IBM_DB & DB2_HELPERS"""
import sys
import ibm_db
from db2_helpers import db_connect, db_connected, db_disconnect, db_load_settings

# --------------------------------------------------
# Database Connection Settings
# --------------------------------------------------
database = "sample"
hostname = "localhost"
hdbc = None

settings = db_load_settings(database, hostname)

if settings:
    hdbc = db_connect(settings)

if not db_connected():
    print("Database connection failed, quitting.")
    sys.exit(1)

mysql = """select distinct tabname
             from syscat.tables
            where tabschema = ?;
"""

mystmt = None
try:
    mystmt = ibm_db.prepare(hdbc, mysql)
    myparms = ("DB2INST1", )

    if ibm_db.execute(mystmt, myparms):
        row = ibm_db.fetch_assoc(mystmt)
        while row:
            print(row['TABNAME'])
            row = ibm_db.fetch_assoc(mystmt)

except Exception as err:
    print("Error executing statement", err)

try:
    ibm_db.free_stmt(mystmt)
except Exception as err:
    print("Error on free statement", err)

db_disconnect()
