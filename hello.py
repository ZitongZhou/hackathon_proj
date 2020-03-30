#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:26:14 2020

@author: zitongzhou
"""

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from main import predict
from toy import toy

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 1)

@app.route('/')
def home():
    return render_template('index.html')
    # return 'This is the home page <h1>HELLO</h1>'

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        alpha = float(request.form["alpha"])
        beta = float(request.form["beta"])
        N = int(request.form["N"])
        Noldmeet = int(request.form["Noldmeet"])
        Nnewmeet = int(request.form["Nnewmeet"])
        Nfriendpool = int(request.form["Nfriendpool"])
        Nsym = int(request.form["Nsym"])
        eg = int(request.form["eg"])
        eg2 = int(request.form["eg2"])
        
        user = request.form["nm"]
        session["user"] = user
        if "user" in session:

            su,prob_1,cpath_1,cpathin_1,prob_2,cpath_2,cpathin_2 = predict(alpha,beta,N,Noldmeet,Nnewmeet,Nfriendpool,Nsym,eg,eg2)
            flash(f"Model successfully loaded!")
            flash(f'number of safe users: {su}')##########number of safe people
            flash(f'Look at user: {eg}')
            flash(f'probability of carrying virus: {prob_1}')
            flash(f'how to get the virus from people with symptom: {cpath_1}')        ######is eg safe or not   all the path from patient with symptom
            flash(f'how to get the virus from people during incubation: {cpathin_1}')      ######is eg safe or not   all the path from patient during incubation
        
            flash(f'Look at user: {eg2}')
            flash(f'probability of carrying virus: {prob_2}')
            flash(f'how to get the virus from people with symptom: {cpath_2}')        ######is eg safe or not   all the path from patient with symptom
            flash(f'how to get the virus from people during incubation: {cpathin_2}')
            
            flash(f'{user}, thank you for using our model.')
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already loaded model!")
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
    
    
    
    
    
    
    
    
    
    