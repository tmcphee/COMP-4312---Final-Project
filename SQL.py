import pymysql.cursors
import subprocess
import os
import threading
from settings import *

#cloud_sql_proxy -instances=<INSTANCE_NAME>>=tcp:3306 -credential_file=credentials.json &
connection = None
proxy_started = False


def sql_connect():
    global connection
    print("SQL CON - > " + SQL_HOST + " ** " +
          SQL_USER + " ** " + SQL_PASSWORD + " ** " + SQL_DB)
    try:
        connection = pymysql.connect(host=SQL_HOST,
                                     user=SQL_USER,
                                     password=SQL_PASSWORD,
                                     db=SQL_DB)
    except Exception as e:
        print("SQL CONNECTION ERROR - Exeception occured:{}".format(e))


def sql_insert(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print("SQL ERROR - Exeception occured:{}".format(e))


def sql_select(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("SQL ERROR - Exeception occured:{}".format(e))
        return [["NA", "**MySQL DB OFFLINE*", "NA"]]


def sql_format_response(content):
    data = [content[0], str(content[1])[2:-1], content[2]]
    return data


def startproxy():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print("IN: " + INSTANCE_NAME)
    print("GAC: " + GOOGLE_APPLICATION_CREDENTIALS)
    if ENVIRONMENT == "Windows":
        proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy.exe")
        subprocess.Popen(proxypath + " -instances=" + INSTANCE_NAME + "=tcp:3306 -credential_file=" + GOOGLE_APPLICATION_CREDENTIALS + " &")
        print("Using Windows style SQL Proxy")
    else:
        proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy")
        subprocess.Popen(proxypath + " -instances=" + INSTANCE_NAME + "=tcp:3306 -credential_file=" + GOOGLE_APPLICATION_CREDENTIALS + " &",
                         shell=True)
        print("Using Linux style SQL Proxy")


def sql_proxy_run():
    try:
        '''t = threading.Thread(target=startproxy())
        t.daemon = True
        t.start()'''
        startproxy()

        sql_connect()
        '''
        retrycount = 3
        if str(connection) is None:
            sql_connect()
            if str(connection) is not None:
                return
            while retrycount != 0:
                print("SQL DB not found. Retrying Connection .. ")
                sql_connect()
                if str(connection) is not None:
                    break
                os.wait(10)
                retrycount -= 1'''
    except Exception as e:
        print("SQL PROXY RUN ERROR - Exeception occured:{}".format(e))

sql_proxy_run()
#sql_insert("DROP TABLE Reviews")
sql_insert("CREATE TABLE Reviews(id int NOT NULL AUTO_INCREMENT, Description BLOB NOT NULL, Response int(1) NOT NULL, PRIMARY KEY (id))")


#TEST CASES
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string', 1)")
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string2', 0)")
#print(sql_select("SELECT * FROM Reviews"))
