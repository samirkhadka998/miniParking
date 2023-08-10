import sqlite3
from flask import Flask, render_template,session, request, redirect
from functools import wraps

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('miniParking.db')
    cur = conn.cursor()
    print(query)
    cur.execute(query, args)
    conn.commit()
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function