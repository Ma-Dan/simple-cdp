import time

from flask import make_response
from flask_httpauth import HTTPTokenAuth
#from authlib.jose import jwt, JoseError
import jwt
from config import SECRET_KEY
from utils.http import auth_err

auth = HTTPTokenAuth(scheme='Bearer')


def generate_token(uid: str):
    header = {'alg': 'HS256'}
    key = SECRET_KEY
    now = time.time()
    data = {'nbf': now, 'exp': now+60*60*24, 'uid': uid}
    token = jwt.encode(data, key, algorithm="HS256")
    return token


@auth.verify_token
def verify_token(token: str):
    key = SECRET_KEY
    try:
        print("verify", token)
        claim = jwt.decode(token, key, algorithms=["HS256"])
        print("claim", claim)
        #claim.validate()
    #except JoseError as e:
    except jwt.ExpiredSignatureError:
        #print(e.error)
        print('token has expired')
        return False
    except jwt.exceptions.InvalidSignatureError:
        print('invalid signature')
        return False
    except:
        print('jwt error')
        return False
    return claim.get('uid')


def unauthorized():
    return make_response(auth_err(), 401)
