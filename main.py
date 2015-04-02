import json

from flask import Flask, g, send_from_directory

import db


app = Flask('world-weaver')


def api_response(func):
    def wrapped(*args, **kwargs):
        out = func(*args, **kwargs)
        if out and out.body:
            out = out.body
        elif out and out._fetch:
            out = out._fetch()

        return json.dumps(out)

    return wrapped


def use_db(func):
    def wrapped(*args, **kwargs):
        conn = getattr(g, '_database', None)
        if not conn:
            conn = g._database = db.setup()
        return func(conn, *args, **kwargs)

    return wrapped


@app.route('/')
def index():
    with open('static/index.html') as f:
        return f.read()


@app.route('/nodes/root')
@api_response
@use_db
def root_node(conn):
    return db.get_root_node(conn)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.teardown_appcontext
def close_db(exception):
    conn = getattr(g, '_database', None)
    if conn:
        conn.close()


if __name__ == '__main__':
    db.setup()

    app.debug = True
    app.run()
