#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:26:14 2020

@author: zitongzhou
"""

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from toy import toy

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 5)

@app.route('/')
def home():
    return render_template('index.html')
    # return 'This is the home page <h1>HELLO</h1>'

@app.route('/test')
def test():
    return render_template('new.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        age = request.form['age']
        session["user"] = user
        session['age'] = age
        next_age = toy(age)
        flash("Login successful!")
        flash(f'next year, {user} will be {next_age} years old.')
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return render_template('user.html', user = user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user}, you have been logged out successfully!", "info")
    
        session.pop("user", None)
    else:
        flash('no login.')
    return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug = True)