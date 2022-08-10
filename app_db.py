import sqlite3
import os
from FDataBase import ExBase
from flask import Flask, render_template, request, g


# config
DATABASE = '/tmp/fl_les.db'
DEBUG = True
SECRET_KEY = 'beaberaberfgbrtgbrfgbfg'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fl_les.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3
    return conn


def create_db():
    try:
        db = connect_db()
        with app.open_resource('sq_db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
    except Exception as e:
        print(e)


def get_db():
    """ Соединение с БД, если оно не установлено"""
    try:
        if not hasattr(g, 'link_db'):
            g.link_db = connect_db()
        return g.link_db
    except:
        print('Could not connect db')


@app.route('/')
def index():
    db = get_db()
    # dbase = ExBase(db)
    return render_template('index.html', menu=ExBase(db).getMenu())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
