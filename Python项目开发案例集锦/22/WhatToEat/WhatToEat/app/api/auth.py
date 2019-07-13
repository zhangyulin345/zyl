from flask import g
from flask_httpauth import  HTTPTokenAuth
from .errors import error_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..models import User

token_auth = HTTPTokenAuth()
serializer = Serializer('mrsoft')

@token_auth.verify_token
def verify_token(token):
    try:
        data = serializer.loads(token)    # 验证token
    except:
        return False
    if 'user_id' in data:
        user = User.query.filter_by(id=data['user_id']).first()
        if user:
            g.user = user
            return True
    return False

@token_auth.error_handler
def token_auth_error():
    return error_response(401)



