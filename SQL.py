import pymysql.cursors
import subprocess
import os
import threading
import signal
from settings import *

#cloud_sql_proxy -instances=<INSTANCE_NAME>>=tcp:3306 -credential_file=credentials.json &
connection = None
proxy_started = False
proxy_instance = None
SQL_INITIAL_CONNECT = False


def sql_connect():
    global connection, SQL_INITIAL_CONNECT
    try:
        connection = pymysql.connect(host=SQL_HOST,
                                     user=SQL_USER,
                                     password=SQL_PASSWORD,
                                     db=SQL_DB)
    except Exception as e:
        print("SQL CONNECTION ERROR - Exeception occured:{}".format(e))


def startproxy():
    global proxy_instance, SQL_INITIAL_CONNECT
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    if ENVIRONMENT == "Windows":
        proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy.exe")
        proxy_instance = subprocess.Popen(proxypath + " -instances=" + INSTANCE_NAME + "=tcp:3306 -credential_file=" + GOOGLE_APPLICATION_CREDENTIALS + " &")
        print("Using Windows style SQL Proxy")
    else:
        proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy")
        proxy_instance = subprocess.Popen(proxypath + " -instances=" + INSTANCE_NAME + "=tcp:3306 -credential_file=" + GOOGLE_APPLICATION_CREDENTIALS + " &",
                         shell=True)
        proxy_instance
        print("Using Linux style SQL Proxy")
    SQL_INITIAL_CONNECT = True


def sql_proxy_run():
    try:
        startproxy()
        sql_connect()
    except Exception as e:
        print("SQL PROXY RUN ERROR - Exeception occured:{}".format(e))


# Redial connection to SQL if connection is lost
# Dont try to reconnect if connection is initially lost
def redial_sql():
    try:
        if SQL_INITIAL_CONNECT == False:
            return False
        if proxy_instance != None:
            print("KILLING OLD CONNECTION TO SQL PROXY...")
            try:
                os.kill(proxy_instance.pid, signal.SIGTERM)
            except Exception as e:
                print(e)
        print("REDIALING CONNECTION TO SQL PROXY...")
        sql_proxy_run()
        return True
    except:
        print("CANNOT CONNECT TO SQL DB")
        return False


def sql_insert(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print("SQL insert ERROR - Exeception occured:{}".format(e))


def sql_select(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("SQL select ERROR - Exeception occured:{}".format(e))
        if redial_sql() == True and connection is not None:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        return [["NA", "**MySQL DB OFFLINE*", "NA"]]


def sql_format_response(content):
    data = [content[0], str(content[1])[2:-1], content[2]]
    return data




#
#sql_insert("DROP TABLE Reviews")



#TEST CASES
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string', 1)")
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string2', 0)")
#print(sql_select("SELECT * FROM Reviews"))
