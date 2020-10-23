# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import signal
import datetime
import sys

#TEST
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

    table = "generate a table from SQL DB here"
    return render_template('run.html', content=content, table=table)


if __name__ == '__main__':
    """
    kill -9 $(lsof -i:5000 -t) 2> /dev/null
    """
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=8080, debug=True)
