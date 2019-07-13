from . import api
from .auth import token_auth
from flask import jsonify,request
from app.models import Category,Food,Record
import random
import requests
from config import Config
from app import db


@api.route('/food/category',methods=['POST'])
@token_auth.login_required
def get_category():
    category = Category.query.order_by(Category.order_num.desc()).all() # 获取菜系信息，并根据order_number降序排序
    data = [{'id':0,'name':'全部'}]
    for item in category:
        data.append(
            {
                'id':item.id,
                'name':item.name
            }
        ),
    # 返回结果
    result = {
        "code":200,
        "msg":"请求成功",
        "data": data
    }
    return jsonify(result)

@api.route('/food/list',methods=['POST'])
def get_food():
    cate_id = int(request.values['cateId'])
    if cate_id:
        food = Food.query.filter_by(cate_id=cate_id).all() # 获取菜系信息
    else:
        food = Food.query.all()  # 获取菜系信息
    data = []
    for item in food:
        data.append(item.name),
    random.shuffle(data)    # 打乱次序
    # 返回结果
    result = {
        "code":200,
        "msg":"请求成功",
        "data": data
    }
    return jsonify(result)

@api.route('/food/cookbook',methods=['POST'])
def get_cookbook():
    """
    菜谱列表
    """
    food = request.values['food'] # 接收传递过来的参数
    url = "http://apis.juhe.cn/cook/query.php"
    params = {
        "menu": food,  # 需要查询的菜谱名
        "key":  Config.CookAppKey,  # 应用APPKEY(应用详细页查询)
        "dtype": "json",  # 返回数据的格式,xml或json，默认json
        "pn": "0",  # 数据返回起始下标
        "rn": "5",  # 数据返回条数，最大30
        "albums": "",  # albums字段类型，1字符串，默认数组
    }
    response = requests.get(url=url,params=params)
    data_json = response.json()
    # 获取菜谱异常，返回异常信息
    if (data_json['resultcode'] != '200'):
        result = {
            "code": data_json['resultcode'],
            "msg":  data_json['reason'],
            "data": {}
        }
        return jsonify(result)

    # 获取菜谱正常，返回菜谱信息
    data = []
    for item in data_json['result']['data']:
        data.append(
            {
                'id': item['id'],
                'title':  item['title'],
                'imtro':  item['imtro'],
                'albums': item['albums'][0]
            }
        )
    result = {
        "code": data_json['resultcode'],
        "msg": data_json['reason'],
        "data": data
    }
    return jsonify(result)

@api.route('/food/cookDetail',methods=['POST'])
def get_cook_detail():
    """
    菜谱详情
    """
    id = request.values['id']  # 接收传递过来的参数
    url = "http://apis.juhe.cn/cook/queryid"
    params = {
        "id": id,  # 菜谱的ID
        "key":Config.CookAppKey,# 应用APPKEY
        "dtype": "",  # 返回数据的格式,xml或json，默认json
    }
    response = requests.get(url=url,params=params)
    data_json = response.json()
    # 获取菜谱异常，返回异常信息
    if (data_json['resultcode'] != '200'):
        result = {
            "code": data_json['resultcode'],
            "msg":  data_json['reason'],
            "data": {}
        }
        return jsonify(result)

    # 获取菜谱正常，返回菜谱信息
    data = data_json['result']['data'][0]

    # 处理数据
    ingredients = []
    for item in data['ingredients'].split(';'):
        temp = {}
        name,consumption = item.split(',')
        temp['name'] = name
        temp['consumption'] = consumption
        ingredients.append(temp)
    burden = []
    for item in data['burden'].split(';'):
        temp = {}
        name,consumption = item.split(',')
        temp['name'] = name
        temp['consumption'] = consumption
        burden.append(temp)
    stepPics = []
    for item in data['steps']:
        stepPics.append(item['img'])

    info = {}
    info['title'] = data['title']
    info['albums'] = data['albums'][0]
    info['imtro'] = data['imtro']
    info['ingredients'] = ingredients
    info['burden'] = burden
    info['steps'] = data['steps']
    info['stepPics'] = stepPics
    result = {
        "code": data_json['resultcode'],
        "msg": data_json['reason'],
        "data": info
    }
    return jsonify(result)

@api.route('/food/foodAdd',methods=['POST'])
def foodAdd():
    name = request.values['food']
    cate_id = request.values['cate_id']
    food = Food.query.filter_by(name=name,cate_id=cate_id).first()
    # 如果已经存在
    if food:
        result = {
            "code": 201,
            "msg": '该美食已经存在'
        }
    else:
        # 如果不存在，写入food表
        food = Food(
            name = name,
            cate_id = cate_id
        )
        db.session.add(food)
        db.session.commit()
        result = {
            "code": 200,
            "msg": '添加成功'
        }
    return jsonify(result)

