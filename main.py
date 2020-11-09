# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, request, render_template, make_response
from flask_cors import CORS
import pyexcel
import signal
import datetime
import sys
import json
from model import predict
from SQL import *
from zipfile import ZipFile
from Bucket import *

os.environ['BUCKET_NAME'] = "comp4312_hotel_reviews"
host = "127.0.0.1"

# define the app
DebuggingOn = bool(os.getenv('DEBUG', False))  # Whether the Flask app is run in debugging mode, or not.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'comp4312'
CORS(app)  # needed for cross-domain requests, allow everything by default


def sigterm_handler(_signo, _stack_frame):
    print(str(datetime.datetime.now()) + ': Received SIGTERM')


def sigint_handler(_signo, _stack_frame):
    print(str(datetime.datetime.now()) + ': Received SIGINT')
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigint_handler)


# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/about')
def about():
    content = "about page test"
    return render_template('about.html', content=content)


@app.route('/application')
def application():
    content = "application page test"
    return render_template('application.html', content=content)


@app.route('/bucket')
def bucket():
    return render_template('Bucket.html', list=web_list_blobs(host))


@app.route('/archive', methods=('GET', 'POST'))
def response():
    query = "SELECT * FROM Reviews "
    input = ""
    response = ""
    if request.method == 'POST':
        if 'Delete' in request.form:
            sql_insert("DELETE FROM Reviews WHERE id=" + request.form['Delete'])

        if 'Search' in request.form:
            if request.form['Input'] != "":
                query += "WHERE Description LIKE '%" + request.form['Input'] + "%' "
                if request.form['Response'] == "Happy":
                    query += "AND Response=1 "
                    response = "Happy"
                if request.form['Response'] == "Not Happy":
                    query += "AND Response=0 "
                    response = "Not Happy"
                input = request.form['Input']
            else:
                if request.form['Response'] == "Happy":
                    query += "WHERE Response=1 "
                    response = "Happy"
                if request.form['Response'] == "Not Happy":
                    query += "WHERE Response=0 "
                    response = "Not Happy"

        if 'Download' in request.form:
            if request.form['Input'] != "":
                query += "WHERE Description LIKE '%" + request.form['Input'] + "%' "
                if request.form['Response'] == "Happy":
                    query += "AND Response=1 "
                if request.form['Response'] == "Not Happy":
                    query += "AND Response=0 "
            else:
                if request.form['Response'] == "Happy":
                    query += "WHERE Response=1 "
                if request.form['Response'] == "Not Happy":
                    query += "WHERE Response=0 "
            query += "order by id desc"
            data = sql_to_string(query)
            sheet = pyexcel.get_sheet(file_type="csv", file_content=data)
            outfile = make_response(sheet.csv)
            outfile.headers["Content-Disposition"] = "attachment; filename=Hotel_Reviews.csv"
            outfile.headers["Content-type"] = "text/csv"
            return outfile
        if 'SavetoGCP' in request.form:
            if request.form['Input'] != "":
                query += "WHERE Description LIKE '%" + request.form['Input'] + "%' "
                if request.form['Response'] == "Happy":
                    query += "AND Response=1 "
                if request.form['Response'] == "Not Happy":
                    query += "AND Response=0 "
            else:
                if request.form['Response'] == "Happy":
                    query += "WHERE Response=1 "
                if request.form['Response'] == "Not Happy":
                    query += "WHERE Response=0 "
            query += "order by id desc"
            data = sql_to_string(query)
            sheet = pyexcel.get_sheet(file_type="csv", file_content=data)
            sheet.save_as(filename=request.form['Name'] + ".csv")
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            tmp_path = os.path.join(ROOT_DIR, request.form['Name'] + ".csv")
            upload_file(request.form['Name'] + ".csv", tmp_path)
            os.remove(tmp_path)

    r1 = ""
    r2 = ""
    r3 = ""
    if response == "Happy":
        r1 = "checked"
    else:
        if response == "Not Happy":
            r2 = "checked"
        else:
            r3 = "checked"
    query += "order by id desc"
    table = make_table_response(query)
    return render_template('response.html', table=table, input=input, response=response, r1=r1, r2=r2, r3=r3)


@app.route('/run', methods=('GET', 'POST'))
def run():
    content = ""
    result = ""
    if request.method == 'POST':
        content = request.form['input']
        # ---------------Machine-Learning-Here---------------
        print(content)
        parent_path = os.path.dirname(os.path.abspath(__file__))
        ml_path = os.path.join(parent_path, "Dataset", "LR.pickle")
        result, prob = predict(content, ml_path)
        print(result)
        print(prob)
        # ---------------------------------------------------
        result = result_conv(result)
        sql_insert("INSERT INTO Reviews (Description, Response) "
                   "VALUES ('" + content + "', " + str(happy_not_toint(result)) + ")")
        result = "Result: " + result

    table = make_table("SELECT * FROM Reviews order by id desc LIMIT 3")
    return render_template('run.html', content=content, table=table, result=result)


def sql_to_string(q):
    obj = "Description,Response\n"
    query = sql_select(q)
    for x in query:
        x = sql_format_response(x)
        obj += "" + x[1] + "," + happy_not_tostr(x[2]) + "\n"
    print(obj)
    return obj


def make_table(query):
    table = ""
    query = sql_select(query)
    for x in query:
        x = sql_format_response(x)
        table += "<tr>"
        table += "<td>" + x[1] + "</td>"
        table += "<td>" + happy_not_tostr(x[2]) + "</td>"
        table += "</tr>"
    return table


def make_table_response(query):
    table = ""
    query = sql_select(query)
    for x in query:
        x = sql_format_response(x)
        table += "<tr>"
        table += "<td>" + x[1] + "</td>"
        table += "<td>" + happy_not_tostr(x[2]) + "</td>"
        table += "<td><form method=\"post\"><button type=\"submit\" class=\"btn btn-danger\" name=\"Delete\"value="\
                 + str(x[0]) + ">Delete</button></form></td>"
        table += "</tr>"
    return table


def result_conv(str):
    if str == "happy":
        return "Happy"
    else:
        return "Not Happy"


def happy_not_tostr(value):
    if value == 1:
        return "Happy"
    else:
        return "Not Happy"


def happy_not_toint(str):
    if str == "Happy":
        return 1
    else:
        return 0


def extract_lr():
    path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(path, "Dataset", "LR.pickle")):
        print("LR.zip Not Found -> Extracting")
        zf = ZipFile(os.path.join(path, "Dataset", "LR.zip"), 'r')
        zf.extractall(os.path.join(path, "Dataset"))
        zf.close()
        print("-> Finished Extracting")
    else:
        print("LR.pickle Exists -> Skip Extract")


def read_config(host):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    if host == "127.0.0.1":
        jsonpath = os.path.join(ROOT_DIR, "hotelreviews.conf")
    else:
        jsonpath = os.path.join("config", "hotelreviews.conf")
    with open(jsonpath) as f:
        return json.load(f)


def get_cred_path(host):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    if host == "127.0.0.1":
        return os.path.join(ROOT_DIR, "credentials.json")
    else:
        return os.path.join("config", "credentials.json")


if __name__ == '__main__':
    """
    kill -9 $(lsof -i:5000 -t) 2> /dev/null
    """
    # Default Host
    extract_lr()

    # Allow for alternate host in Dockerfile
    if len(sys.argv) == 2:
        host = sys.argv[1]

    data = read_config(host)
    if data is not None:
        sql_proxy_run(host, data['instance_name'])
        os.environ['BUCKET_NAME'] = data['bucket_name']
        os.environ['SQL_HOST'] = data['SQL_HOST']
        os.environ['SQL_USER'] = data['SQL_USER']
        os.environ['SQL_PASSWORD'] = data['SQL_PASSWORD']
        os.environ['SQL_DB'] = data['SQL_DB']

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = get_cred_path(host)
    create_bk()

    app.run(host=host, port=8080, debug=True)


