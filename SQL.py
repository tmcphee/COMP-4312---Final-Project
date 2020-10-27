import pymysql.cursors

#cloud_sql_proxy -instances=<INSTANCE_NAME>>=tcp:3306 -credential_file=credentials.json &

try:
    connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='comp4312admin',
                             db='hotel_reviews')
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
        return [["NA", "**NA*", "NA"]]


def sql_format_response(content):
    data = [content[0], str(content[1])[2:-1], content[2]]
    return data


sql_insert("DROP TABLE Reviews")
sql_insert("CREATE TABLE Reviews(id int NOT NULL AUTO_INCREMENT, Description BLOB NOT NULL, Response int(1) NOT NULL, PRIMARY KEY (id))")

#TEST CASES
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string', 1)")
#sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('test string2', 0)")
#print(sql_select("SELECT * FROM Reviews"))