import os

from flask import Flask, request, render_template, session, redirect, url_for
# from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
# Session(app)
# socketio = SocketIO(app)

#GLOBAL VARIABLES
user_list = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method  == 'POST':
        username  = request.form.get("username")

        # TODO Remove user user_list when they "leave"
        for user in user_list:
            if  username == user:
                return "Username is already in use. Try another username!"
        
        user_list.append(username)
        session['username'] = username
        return redirect(url_for("chat"))

    return render_template("login.html")

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    return Chatroom

""" TODO
#0 Create basic HTML template
    - Create SCSS file and create container around body

#1 Display Name
    User sign-up page
    Check user list
    Add username to session
    If not available, store user name
    Render chat page
    Add login required decorator

#0.7 Global varariables
    - user list
    - current user
    - messages

#.8 Watch Local Storage 

#2 Render channels/chat page
    - Setup dummy channel and message data
    - Pull channles from messages using Jinja
    - Add create channel button
    - Add leave button
    - Call Ajac to get messages from a channel

#3 Render messages from a channel
    - Pass channel name to AJAX route
    - AJAX call to messages dictoionary

#4 Socket.io
    - Store channel name
    - broadcast message submit after button click
    - listen to message submit from backend server
    - append message to messages dictionary
    - broadcast message submit from backend server
    - listen  to message submit from frontend
    - check message ;ength is less than 100

#5 Get API respponse from something
"""