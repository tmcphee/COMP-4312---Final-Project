import pymysql.cursors
import subprocess
import os

#cloud_sql_proxy -instances=<INSTANCE_NAME>>=tcp:3306 -credential_file=credentials.json &

try:
    connection = pymysql.connect(host=os.environ['SQL_HOST'],
                                 user=os.environ['SQL_USER'],
                                 password=os.environ['SQL_PASSWORD'],
                                 db=os.environ['SQL_DB'])
except Exception as e:
    print("SQL ERROR - Exeception occured:{}".format(e))


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


def sql_proxy_run():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        if os.environ['ENVIRONMENT'] == "Windows":
            proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy.exe")
            subprocess.Popen(proxypath + " -instances=" + os.environ['INSTANCE_NAME'] +"=tcp:3306 -credential_file=" + os.environ['GOOGLE_APPLICATION_CREDENTIALS'] +" &")
        else:
            proxypath = os.path.join(ROOT_DIR, "cloud_sql_proxy")
            subprocess.Popen(proxypath + " -instances=" + os.environ['INSTANCE_NAME'] +"=tcp:3306 -credential_file=" + os.environ['GOOGLE_APPLICATION_CREDENTIALS'] +" &", shell=True)
    except Exception as e:
        print("SQL ERROR - Exeception occured:{}".format(e))


#sql_insert("DROP TABLE Reviews")
sql_insert("CREATE TABLE Reviews(id int NOT NULL AUTO_INCREMENT, Description BLOB NOT NULL, Response int(1) NOT NULL, PRIMARY KEY (id))")

#TEST CASES
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string', 1)")
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string2', 0)")
#print(sql_select("SELECT * FROM Reviews"))
