from http import HTTPStatus

from flask import Request, json, jsonify


def parse_request(req: Request):
    data: dict = json.loads(req.get_data().decode('utf-8'))
    return data

def _http_response(code, message, result, status):
    return jsonify({'code': code, 'message': message, 'result': result, 'status': status})

def success(message='', result=None, status=True):
    return _http_response(HTTPStatus.OK, message, result, status)

def param_err(message='', result=None, status=False):
    return _http_response(HTTPStatus.BAD_REQUEST, message, result, status)

def auth_err(message='', result=None, status=False):
    return _http_response(HTTPStatus.UNAUTHORIZED, message, result, status)

def server_err(message='', result=None, status=False):
    return _http_response(HTTPStatus.INTERNAL_SERVER_ERROR, message, result, status)
