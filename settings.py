import json
import os
import sys

HOST = "127.0.0.1"
ENVIRONMENT = os.environ.get('INSTANCE_NAME')
INSTANCE_NAME = os.environ.get('INSTANCE_NAME')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
SQL_HOST = os.environ.get('SQL_HOST')
SQL_USER = os.environ.get('SQL_USER')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
SQL_DB = os.environ.get('SQL_DB')
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


def find_conf_files():
    global GOOGLE_APPLICATION_CREDENTIALS
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        path1 = os.path.join(ROOT_DIR, "credentials.json")
        if os.path.isfile(path1):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path1
            GOOGLE_APPLICATION_CREDENTIALS = path1
            jsonpath = os.path.join(ROOT_DIR, "hotelreviews.conf")
            with open(jsonpath) as f:
                return json.load(f)
        else:
            path2 = os.path.join("config", "credentials.json")
            if os.path.isfile(path2):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path2
                GOOGLE_APPLICATION_CREDENTIALS = path2
                jsonpath = os.path.join("config", "credentials.json")
                with open(jsonpath) as f:
                    return json.load(f)
        print("ERROR - Files not found")
        return None
    except Exception as e:
        print("ERROR - CONFIG Files not found - Exeception occured:{}".format(e))
        return None


if 'HOST' in os.environ:
    HOST = os.environ.get('HOST')


# Check if the user defined a host as an argument
if len(sys.argv) == 2:
    HOST = sys.argv[1]

# Allow for alternate host in Dockerfile
# if host is 127.0.0.1 assume user is running on windows
# if host is 0.0.0.0 assume user is running in Linux (Docker)
if HOST == "127.0.0.1":
    ENVIRONMENT = "Windows"
else:
    ENVIRONMENT = "Linux"

# Check if user defined a config file
# if not the user can define the env variables manually
data = find_conf_files()
if data is not None:
    print(data)
    INSTANCE_NAME = data['INSTANCE_NAME']
    BUCKET_NAME = data['BUCKET_NAME']
    SQL_HOST = data['SQL_HOST']
    SQL_USER = data['SQL_USER']
    SQL_PASSWORD = data['SQL_PASSWORD']
    SQL_DB = data['SQL_DB']

