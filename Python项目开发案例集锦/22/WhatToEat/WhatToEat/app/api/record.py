from . import api
from .auth import token_auth
from flask import jsonify,request,g
from app.models import Category,Food,Record
from app import db

@api.route('/record/add',methods=["POST"])
@token_auth.login_required
def record_add():
    food = request.values['food']        # 获取美食ID
    user_id = g.user.id                  # 获取用户ID
    record = Record.query.filter_by(user_id=user_id,food=food).first()
    try:
        if record:                        # 如果记录已经存在，则更改选择美食次数
            record.number += 1
            db.session.add(record)
            db.session.commit()
        else :                          # 如果记录不存在，则将美食次数设置为1
            record = Record(
                user_id = user_id,
                food = food,
                number = 1
            )
            db.session.add(record)
            db.session.commit()
        result = {
            "code": '200',
            "msg": '记录成功',
        }
    except:
        result = {
            "code": '201',
            "msg": '记录失败',
        }
    return jsonify(result)

@api.route('/record/list',methods=["POST"])
@token_auth.login_required
def record_list():
    user_id = g.user.id
    record = Record.query.filter_by(user_id=user_id).all()
    if not record:
        result = {
            "code": '200',
            "msg": '暂无数据',
            "data": ''
        }
        return jsonify(result)
    data = []
    for item in record:
        temp = {
            "name": item.food,
            "value": item.number
        }
        data.append(temp)
    result = {
        "code": '200',
        "msg": 'success',
        "data": data
    }
    return jsonify(result)

@api.route('/record/clear',methods=["POST"])
@token_auth.login_required
def record_clear():
    user_id = g.user.id
    try:
        record = Record.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        result = {
            "code": '200',
            "msg": '清除数据成功',
        }
    except:
        result = {
            "code": '200',
            "msg": '清除数据失败',
        }
    return jsonify(result)

