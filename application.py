import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

""" TODO  
Define global local storage variables. Current user and current channel
"""


@app.route("/")
def index():
    return render_template("login.html")

""" TODO
#0 Create basic HTML template
#0.5 Setup dummy channel and message data
#0.8 Global varariables
    - user list
    - current user
    - messages

#1 Display Name
    User sign-up page
    Check local storage for user name
    If not available, store user name
    Render chat page

#2 Render channels/chat page
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