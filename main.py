# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import signal
import datetime
import sys
#from SQL import *

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
    return render_template('index.html')


@app.route('/about')
def about():
    content = "about page test"
    return render_template('about.html', content=content)


@app.route('/application')
def application():
    content = "application page test"
    return render_template('application.html', content=content)


@app.route('/run', methods=('GET', 'POST'))
def run():
    content = ""
    if request.method == 'POST':
        content = request.form['input']
        print(content)
        #sql_insert("INSERT INTO Reviews (Description, Response) VALUES ('" + content + "', 1)")

    table = "generate a table from SQL DB here"
    #table = make_table("SELECT * FROM Reviews order by id desc LIMIT 3")
    return render_template('run.html', content=content, table=table)

#Works comment out so no need to start DB everytime
'''
def make_table(query):
    table = ""
    query = sql_select(query)
    for x in query:
        x = sql_format_response(x)
        table += "<tr>"
        table += "<td>" + x[1] + "</td>"
        table += "<td>" + yes_no(x[2]) + "</td>"
        table += "</tr>"
    return table
'''


def yes_no(value):
    if value==1:
        return "Happy"
    else:
        return "Not Happy"


if __name__ == '__main__':
    """
    kill -9 $(lsof -i:5000 -t) 2> /dev/null
    """
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=8080, debug=True)
