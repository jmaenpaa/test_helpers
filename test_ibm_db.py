""" Example program using IBM_DB against Db2"""
# import os
import sys
import getpass
import platform
import ibm_db
from db2_helpers import db_load_settings

# --------------------------------------------------
# Database Connection Settings
# --------------------------------------------------
database = "sample"
hostname = "localhost"
environment = "dev"

# Load saved connection settings (set by db_credentials command)
settings = db_load_settings(database, hostname)

if not settings:
    print("You need to create the database connection settings with db_credentials")
    sys.exit(1)

connect_string = "DRIVER={IBM DB2 ODBC DRIVER}" + ";"
connect_string += "DATABASE=" + database + ";"
connect_string += "HOSTNAME=" + hostname + ";"
connect_string += "PROTOCOL=TCPIP;PORT=" + settings["port"] + ";"
connect_string += "UID=" + settings["uid"] + ";"
connect_string += "PWD=" + settings["pwd"] + ";"

connect_options = {"SQL_ATTR_INFO_PROGRAMNAME": "JHMTESTHELPERS",  # 20 char max
                   "SQL_ATTR_INFO_USERID": getpass.getuser(),  # 255 char max
                   "SQL_ATTR_INFO_WRKSTNNAME": platform.node()  # 255 char max
                   }
# --------------------------------------------------
hdbc = None  # Connection Handle
# --------------------------------------------------

try:
    hdbc = ibm_db.connect(connect_string, "", "", connect_options)
except Exception as err:
    print("connection failed with", err)
    sys.exit(1)

if hdbc:
    print("connected")

# --------------------------------------------------
# Query 1
# --------------------------------------------------
print("\nQuery1 begin")

my_sql = """select distinct tabschema, tabname
             from syscat.tables
            where tabschema = 'DB2INST1';
"""
my_stmt = None

try:
    my_stmt = ibm_db.prepare(hdbc, my_sql)
except Exception as err:
    print("Error on Prepare", err)

try:
    rc = ibm_db.execute(my_stmt)
    if rc:
        try:
            row = ibm_db.fetch_assoc(my_stmt)
            while row:
                print(row["TABSCHEMA"], row["TABNAME"])
                row = ibm_db.fetch_assoc(my_stmt)
        except Exception as err:
            print("Error on Fetch", err)
    else:
        print("Execute failed")

except Exception as err:
    print("Error on Execute", err)

# --------------------------------------------------
# Query 2
# --------------------------------------------------
print("\nQuery2 begin")

my_sql = """select distinct tabschema, tabname
             from syscat.tables
            where tabschema = ?
              and type = ?;
"""

my_params = ("DB2INST1", "T")

try:
    my_stmt = ibm_db.prepare(hdbc, my_sql)
except Exception as err:
    print("Error on Prepare", err)

try:
    rc = ibm_db.execute(my_stmt, my_params)
    if rc:
        column_name1 = ibm_db.field_name(my_stmt, 0)
        column_name2 = ibm_db.field_name(my_stmt, 1)

        try:
            row = ibm_db.fetch_assoc(my_stmt)
            print(column_name1, column_name2)
            while row:
                print(row["TABSCHEMA"], row["TABNAME"])
                row = ibm_db.fetch_assoc(my_stmt)
        except Exception as err:
            print("Error on Fetch", err)
    else:
        print("Execute failed")
except Exception as err:
    print("Error on Execute statement", err)

try:
    ibm_db.free_stmt(my_stmt)
except Exception as err:
    print("Error on free statement", err)

# --------------------------------------------------
# Clean up
# --------------------------------------------------
if hdbc:
    ibm_db.close(hdbc)
    print("disconnected")

print("done")
