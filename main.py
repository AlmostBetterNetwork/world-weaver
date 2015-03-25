from flask import Flask

import db


app = Flask('world-weaver')

@app.route('/')
def index():
    return 'Welcome'


db.setup()

@app.teardown_appcontext
def teardown(exception):
    db.teardown()

if __name__ == '__main__':
    app.run()
