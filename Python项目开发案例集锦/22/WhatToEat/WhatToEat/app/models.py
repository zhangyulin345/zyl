from . import db
from datetime import datetime

# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)                         # 编号
    openid = db.Column(db.String(50),)                                   # 微信用户id
    nickname = db.Column(db.String(100))                                 # 微信昵称
    phone = db.Column(db.String(11), unique=True)                        # 手机号
    avatar = db.Column(db.String(200))                                   # 微信头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间

    def __repr__(self):
        return '<User %r>' % self.name


# 美食表
class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    name = db.Column(db.String(100))                                     # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加景区时间
    cate_id = db.Column(db.Integer, db.ForeignKey('category.id'))        # 所属菜系

    def __repr__(self):
        return "<Food %r>" % self.name

# 菜系表
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    name = db.Column(db.String(255),unique=True)                        # 标题
    order_num = db.Column(db.Integer,default=0)                          # 序号
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    food = db.relationship("Food", backref='category')                  # 外键关系关联

# 订餐表
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)            # 编号
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) # 用户id
    food = db.Column(db.String(255))                         # 食物
    number = db.Column(db.Integer)                           # 下单次数
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 下单时间

    def __repr__(self):
        return "<Record %r>" % Record.id

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    name = db.Column(db.String(100), unique=True)                       # 管理员账号
    pwd = db.Column(db.String(100))                                     # 管理员密码

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)
