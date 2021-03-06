import os
import requests
from datetime import datetime

from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from helper import login_required

app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
socketio = SocketIO(app)

#Set Giphy API key from environemnt
giphy_key = os.environ['GIPHY']

#GLOBAL VARIABLES
user_list = []
messages = {"general": [['patrick', 'hello', '8:45pm'], ['michelle', 'hola', '8:46pm'], ['patrick', 'i wuv u', '9pm']], "Flask": [], "Fronted": [], "CLI": [], "Random": [['pat', 'i luv oj', '8:45pm'], ['mich', 'wut?', '8:46pm'], ['pat', 'i wuv u', '9pm']]}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method  == 'POST':
        username  = request.form.get("username")

        for user in user_list:
            if  username == user:
                return "Username is already in use. Try another username!"
        
        #TODO do client side disabling
        if username == None:
            return "Username is empty. Try again."
        
        user_list.append(username)
        session['username'] = username
        return redirect(url_for("chat"))

    return render_template("login.html")

@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        channel = request.form.get('channel')

        #TODO channel not being stored
        messages[channel] = []

        return jsonify({"channel": channel})

    return render_template('chat.html', username=session['username'], channels=messages.keys())

@app.route("/messages", methods=['GET', 'POST'])
@login_required
def getmessage():
    if request.method == 'POST':
        channel = request.form.get('channel')
        message_list = messages[channel]

        return jsonify(message_list)

    return "Does not support GET request"

@socketio.on("send msg")
def send(data):
    msg = data["msg"]
    
    # Store message to right channel with timestamp and username
    time = datetime.now().time().strftime("%H:%M %p")
    username = session['username']
    body = msg[0]
    curr_chnnl = msg[1]
    
    # check if message is a giphy command
    if body[0:6] == "/giphy":
        payload = {'api_key': giphy_key, 's': body[8:], 'weirdness': 6}
        r = requests.get('http://api.giphy.com/v1/gifs/translate?', params=payload)
        giphyObj = r.json()
        body = giphyObj['data']['images']['downsized_small']['mp4']
    
    # Check legnth of messages and remove oldest message
    if len(messages[curr_chnnl]) >= 100:
        messages[curr_chnnl].pop(0)

    # Store message into global variable
    messages[curr_chnnl].append([username, body, time])
    
    # create broadcast message and  emit
    broadcast = [username, body, time, curr_chnnl]
    emit('broadcast msg', {'msg': broadcast}, broadcast=True)

@app.route("/leave")
def leave():
    user_list.pop(user_list.index(session['username']))
    session.clear()
    return redirect(url_for('index'))


""" TODO
#0 Create basic HTML template
    - Create SCSS file and create container around body

#1 Display Name
    User sign-up page
    Check user list
    Add username to session
    If not available, store user name
    Add helper and login required decorator
    Render chat page
    - Add leave button

#1.5 Global varariables
    - user list
    - current user
    - messages

#2 Render channels/chat page
    - Setup dummy channel 
    - Pull channles from messages using Jinja
    - Add create channel button
    - Call Ajax to get messages from a channel

#3 Render messages from a channel
    - set dummy message data (time / message / user / )
    - Pass channel name to AJAX route
    - AJAX call to messages dictoionary
    - store current channel in local storagee

#4 Socket.io
    - Need to figure out why button click event not working
    - Store channel name
    - broadcast message submit after button click
    - listen to message submit from backend server
    - check message length is less than 100
        - append message to messages dictionary
    - broadcast message submit from backend server
    - listen  to message submit from frontend

#5 Improvements
    - For initial login load general messages
        - Factor out message loading to function
    - Fix datetime not showing / replace channel to username
    - Prevent new messages from loading in other channels
    -  each user needs its own channel state
    - message is being all stoed into general channel
    - Prevent duplicate channels
    - Disable button when empty. Clear form once submitted.
    
    
#5 Get API respponse from something
    - enable image render: https://stackoverflow.com/questions/30911578/javascript-render-an-image-from-a-link
        - create XML request
        - Parse Object
        - Render URL as image
        - Append to list
    - Pop messages over 100
    - prepare gitignore file
"""