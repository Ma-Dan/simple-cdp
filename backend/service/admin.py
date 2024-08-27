from flask import Blueprint, Flask, make_response, render_template, request
from flask_cors import cross_origin
import json

#数据库服务
from components.database import db, User

# 认证服务
from utils.bcrypt import hash_pwd, compare_pwd
from utils.http import parse_request, _http_response, success, param_err, auth_err, server_err
from components.authenticate import auth, generate_token, verify_token

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True, expose_headers='access_token')
def login():
    data = parse_request(request)
    username = data.get('username')
    password = data.get('password')
    print(username, password)
    user = User.select().where(User.username == username).first()
    if not user or not compare_pwd(password, user.password):
        return make_response(param_err('用户名或密码错误'))
    token = generate_token(user.id)
    user = {'username': user.username, "userid": user.id, "role": user.role, "token": token}
    response = make_response(success('登录成功', user))
    response.headers['access_token'] = token
    return response


@admin_api.route('/api/register', methods=['POST'])
def register():
    data = parse_request(request)
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    print(username, password, role)
    if User.select().where(User.username == username):
        return make_response(param_err('用户名已存在'))
    user = User.create(username=username, password=hash_pwd(password), role=role)
    if not user:
        return make_response(server_err('内部错误，创建失败'))
    token = generate_token(user.id)
    user = {'username': user.username, 'role': user.role}
    response = make_response(success('注册成功，将自动跳转', user))
    response.headers['access_token'] = token
    return response