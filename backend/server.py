from flask import Flask, make_response, render_template, request
from flask_cors import CORS
from flask_cors import cross_origin
from flask_socketio import SocketIO, Namespace, emit, disconnect, join_room, leave_room
import numpy as np
import base64
import os
import json
import time
import urllib

from config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

# 认证服务
from components.authenticate import verify_token

# Websocket服务
socket = SocketIO(logger=True, engineio_logger=True)

# 用户管理
from service.admin import admin_api
app.register_blueprint(admin_api)

from service.data import data_api
app.register_blueprint(data_api)

# Websocket服务
def authenticate():
    # 获取客户端发送的认证信息
    token = request.args.get('token')

    # 进行身份验证
    return verify_token(token)

@socket.on('connect')
def connect():
    if not authenticate():
        return False
    print('connected')

@socket.on('disconnect')
def disconnect():
    token = request.args.get('token')
    print('disconnect')

@socket.on('user_login')
def user_login(username: str):
    print(f'{username} login')

@socket.on('join_room')
def on_join(username: str, room_id: str):
    join_room(room_id)
    print(f'{username} join {room_id}')

@socket.on('leave_room')
def on_leave(username: str, room_id: str):
    print(f'{username} leave {room_id}')
    leave_room(room_id)

@socket.on('send_message')
def handle_message(content: str, username: str, avatar: str, room_id: str):
    pass


def register_components(app: Flask):
    socket.init_app(app, cors_allowed_origins='*')
    app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

if __name__ == '__main__':
    register_components(app)
    socket.run(app, host='0.0.0.0', port=8087)