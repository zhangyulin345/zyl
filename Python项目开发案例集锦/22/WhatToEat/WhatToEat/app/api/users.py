from . import api
from flask import request,jsonify,g
from app.models import User,Category
from app.libs.MemberService import MemberService
from app import db
from .auth import serializer

@api.route('/user/login',methods=['POST'])
def login():
    '''
    授权登录
    '''
    req = request.values # 接收数据
    nickname = req['nickName'] if 'nickName' in req else ''    # 获取昵称
    avatar   = req['avatarUrl'] if 'avatarUrl' in req else ''  # 获取头像
    # 判断code 是否存在
    code = req['code'] if 'code' in req else ''
    if not code or len( code ) < 1:
        result = {
            "code": 201,
            "msg": "需要微信授权code",
            "data": {}
        }
        return jsonify(result)

    # 根据code,获取openid
    openid = MemberService.getWeChatOpenId( code )
    if openid is None:
        result = {
            "code":201,
            "msg":"调用微信出错",
            "data":{}
        }
        return jsonify(result)

    # 如果用户存在，写入member表中
    user = User.query.filter_by(openid=openid).first()
    if not user:
        user = User(
            openid   = openid,
            nickname = nickname,
            avatar   = avatar,
        )
        db.session.add(user)
        db.session.commit()
    token = serializer.dumps({'user_id': user.id})       # 生成token
    # 返回结果
    result = {
        "code":200,
        "msg":"登录成功",
        "data":
            {"userInfo":
                 {
                     "nickName": user.nickname,
                     "avatarUrl": user.avatar,
                 },
            "token": token.decode(),                    # byte 转化为string
            }
    }
    return jsonify(result)

