# _*_ coding:utf-8 _*_
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from app.admin.forms import LoginForm,PwdForm,CategoryForm,FoodForm,TravelsForm
from app.models import Admin,Category,User,Food,Record
from sqlalchemy import or_
from functools import wraps


def admin_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login
def index():
    return render_template("admin/index.html")

@admin.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录功能
    """
    form = LoginForm()   # 实例化登录表单
    if form.validate_on_submit():   # 验证提交表单
        data = form.data    # 接收数据
        admin = Admin.query.filter_by(name=data["account"]).first() # 查找Admin表数据
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!", "err")   # 闪存错误信息
            return redirect(url_for("admin.login")) # 跳转到后台登录页
        # 如果是正确的，就要定义session的会话进行保存。
        session["admin"] = data["account"]  # 存入session
        session["admin_id"] = admin.id # 存入session
        return redirect(url_for("admin.index")) # 返回后台主页

    return render_template("admin/login.html",form=form)    

@admin.route('/logout/')
@admin_login
def logout():
    """
    后台注销登录
    """
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))

@admin.route('/pwd/',methods=["GET","POST"])
@admin_login
def pwd():
    """
    后台密码修改
    """
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


@admin.route("/user/list/", methods=["GET"])
@admin_login
def user_list():
    """
    会员列表
    """
    page = request.args.get('page', 1, type=int) # 获取page参数值 
    keyword = request.args.get('keyword', '', type=str)

    if keyword:
        # 根据姓名或者邮箱查询
        filters = or_(User.nickname == keyword, User.openid == keyword)
        page_data = User.query.filter(filters).order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:
        page_data = User.query.order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)

    return render_template("admin/user_list.html", page_data=page_data)


@admin.route("/user/view/<int:id>/", methods=["GET"])
@admin_login
def user_view(id=None):
    """
    查看会员详情
    """
    from_page = request.args.get('fp')
    if not from_page:
        from_page = 1
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user, from_page=from_page)

@admin.route('/category/add/',methods=["GET","POST"])
@admin_login
def category_add():
    """
    添加菜系
    """
    form = CategoryForm()
    if form.validate_on_submit():
        data = form.data # 接收数据
        category = Category.query.filter_by(name=data["name"]).count()
        # 说明已经有这个菜系了
        if category == 1:
            flash("菜系已存在", "err")
            return redirect(url_for("admin.category_add"))
        category = Category(
            name=data["name"],
            order_num = int(data['order_num'])
        )
        db.session.add(category)
        db.session.commit()
        flash("菜系添加成功", "ok")
        return redirect(url_for("admin.category_add"))
    return render_template("admin/category_add.html",form=form)

@admin.route("/category/edit/<int:id>", methods=["GET", "POST"])
@admin_login
def category_edit(id=None):
    """
    菜系编辑
    """
    form = CategoryForm()
    form.submit.label.text = "修改"
    category = Category.query.get_or_404(id)
    if request.method == "GET":
        form.name.data = category.name
        form.order_num.data = category.order_num
    if form.validate_on_submit():
        data = form.data
        category_count = Category.query.filter_by(name=data["name"]).count()
        if category.name != data["name"] and category_count == 1:
            flash("菜系已存在", "err")
            return redirect(url_for("admin.category_edit", id=category.id))
        category.name = data["name"]
        category.is_recommended = int(data["order_num"])
        db.session.add(category)
        db.session.commit()
        flash("菜系修改成功", "ok")
        return redirect(url_for("admin.category_edit", id=category.id))
    return render_template("admin/category_edit.html", form=form, category=category)


@admin.route("/category/list/", methods=["GET"])
@admin_login
def category_list():
    """
    标签列表
    """
    name = request.args.get('name',type=str)     # 获取name参数值
    page = request.args.get('page', 1, type=int) # 获取page参数值   
    if name: # 搜索功能
        page_data = Category.query.filter_by(name=name).order_by(
            Category.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:   
        # 查找数据
        page_data = Category.query.order_by(
            Category.addtime.desc()
        ).paginate(page=page, per_page=5)
    return render_template("admin/category_list.html", page_data=page_data) # 渲染模板


@admin.route("/category/del/", methods=["GET"])
@admin_login
def category_del():
    """
    菜系删除
    """
    id = request.args.get('id')
    res = {}
    try:
        category = Category.query.filter_by(id=id).first_or_404()
        food = Food.query.filter_by(cate_id=id).count()
        if food:
            res['status'] = -2
            res['message'] = "菜系<<{0}>>删除失败,请先删除该菜系下的菜品".format(category.name)
        else:
            res['status']  = 1
            res['message'] =  "菜系<<{0}>>删除成功".format(category.name)
            db.session.delete(category)
            db.session.commit()
    except:
        res['status']  = -1
        res['message'] =  "菜系<<{0}>>删除失败".format(category.name)
    return jsonify(res)


@admin.route("/food/add/", methods=["GET", "POST"])
@admin_login
def food_add():
    """
    添加菜品页面
    """
    form = FoodForm() # 实例化form表单
    form.cate_id.choices = [(v.id, v.name) for v in Category.query.all()] # 为cate_id添加属性
    if form.validate_on_submit():
        data = form.data
        # 判断景区是否存在    
        food_count = Food.query.filter_by(name=data["name"]).count()
        # 判断是否有重复数据。
        if food_count == 1 :
            flash("菜品已经存在！", "err")
            return redirect(url_for('admin.food_add'))

        # 为Scenic类属性赋值
        food = Food(
            name=data["name"],
            cate_id = data["cate_id"],
        )
        db.session.add(food)  # 添加数据
        db.session.commit()     # 提交数据
        flash("添加美食成功！", "ok") # 使用flash保存添加成功信息
        return redirect(url_for('admin.food_add')) # 页面跳转
    return render_template("admin/food_add.html", form=form) # 渲染模板

@admin.route("/food/list/", methods=["GET"])
@admin_login
def food_list():
    """
    菜品列表页面
    """
    name = request.args.get('name','',type=str)   # 获取查询标题
    page = request.args.get('page', 1, type=int)   # 获取page参数值
    if name :                                     # 根据名称搜索景区
        page_data = Food.query.filter(Food.name.like("%" + name + "%")).order_by(
            Food.addtime.desc()                    # 根据添加时间降序
        ).paginate(page=page, per_page=5)          # 分页
    else :                                         # 显示全部菜品
        page_data = Food.query.order_by(
            Food.addtime.desc()                  # 根据添加时间降序
        ).paginate(page=page, per_page=5)          # 分页
    return render_template("admin/food_list.html", page_data=page_data) # 渲染模板

@admin.route("/food/edit/<int:id>/", methods=["GET", "POST"])
@admin_login
def food_edit(id=None):
    """
    编辑景区页面
    """
    form = FoodForm() # 实例化ScenicForm类
    form.cate_id.choices = [(v.id, v.name) for v in Category.query.all()]  # 为cate_id添加属性
    food = Food.query.get_or_404(int(id)) # 根据ID查找景区是否存在
    if request.method == "GET":        # 如果以GET方式提交，获取所有景区信息
        form.cate_id.data = food.cate_id
    if form.validate_on_submit():     # 如果提交表单
        data = form.data              # 获取表单数据
        food_count = Food.query.filter_by(name=data["name"]).count()  # 判断标题是否重复
        # 判断是否有重复数据
        if food_count == 1 and food.name != data["name"]:
            flash("菜品已经存在！", "err")
            return redirect(url_for('admin.food_edit', id=id))

        # 属性赋值
        food.name = data["name"]
        food.cate_id = data["cate_id"]
        db.session.add(food)   # 添加数据
        db.session.commit()    # 提交数据
        flash("修改菜品成功！", "ok")
        return redirect(url_for('admin.food_edit', id=id)) # 跳转到编辑页面
    return render_template("admin/food_edit.html", form=form, food=food) # 渲染模板，传递变量


@admin.route("/food/", methods=["GET"])
@admin_login
def food_del():
    """
    菜品删除
    """
    id = request.args.get('id')
    res = {}
    try:
        food = Food.query.filter_by(id=id).first_or_404()
        res['status']  = 1
        res['message'] =  "菜品<<{0}>>删除成功".format(food.name)
        db.session.delete(food)
        db.session.commit()
    except:
        res['status']  = -1
        res['message'] =  "菜品<<{0}>>删除失败".format(food.name)
    return jsonify(res)






