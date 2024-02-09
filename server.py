import functools
from flask import send_from_directory
from flask_login import current_user, login_required
from flask_socketio import disconnect, emit, SocketIO
from project import create_app

app, socketio = create_app(testing=True)

import os

    
@app.route('/<path:path>')
@login_required
def send_report(path:str):
    if(path.startswith("js/") or path.startswith("css/") or path.startswith("img/") and os.path.exists("dist/"+path)):# and not path.endswith(".svg")):
        return send_from_directory('../dist', path)
    elif(path.startswith("/container"))  and os.path.exists(path):
        return send_from_directory('.', path)
    else:
        return defau()

@app.route('/index.html')
@login_required
def defau():
    path ="index.html"
    resp =  send_from_directory('../dist', path)
    return resp


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

"""@socketio.on('join')
#@authenticated_only
def handle_my_custom_event(data):
    emit('my response', {'message': '{0} has joined'.format(current_user.name)},
         broadcast=True)
"""
    
socketio.run(app, "0.0.0.0", port=8087)