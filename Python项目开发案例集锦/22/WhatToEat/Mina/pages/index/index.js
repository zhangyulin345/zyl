//获取应用实例
const app = getApp()
const timer = null
Page({
  data: {
    userInfo: {},
    categories: [],
    categoryIndex: 0,
    btnText:'开始',
    isProcess:false,
    dishes:[],
    food: "今天吃什么呢？",
  },
  // 加载页面
  onLoad: function () {
    this.getCategory()  // 获取菜系分类信息
    this.getFood(0)     // 获取食物信息，默认获取全部美食
  },
  onShow: function (){
    // 判断是否登录
    var that = this
    wx.checkSession({
      success: function () {
        //session_key 未过期，并且在本生命周期一直有效
        that.setData({
            userInfo: app.globalData.userInfo
        })
        return ;
      },
      fail: function () {
        // session_key 已经失效，需要重新执行登录流程
        wx.navigateTo({
          url: "../login/login"
        })
      }
    })
  },
  // 获取菜系分类信息
  getCategory: function(){
      var value = app.getCache('categories')                    // 从缓存中取值
      if (!value) {                                               // 如果缓存不存在，再从request请求获取
        var that = this
        wx.request({
            url: 'http://127.0.0.1:5000/api/food/category', // 请求URL
            method: 'POST',                                      // 请求方式为POST
            header:app.getRequestHeader(),                        //  设置header参数，使用Bearer Token方式访问资源
            success: function (response) {                      // 请求成功后操作
              app.setCache('categories',response.data.data)     // 写入缓存
              that.setData({
                categories: response.data.data                   // 为categories 页面变量赋值
              });
            }
        })
      }
      this.setData({                                            // 为categories 页面变量赋值
        categories: value
      });
  },
  // 获取美食信息
  getFood: function(cateId) {
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:5000/api/food/list',     // 请求接口
        method: 'POST',                                     // 请求方式为POST
        header:app.getRequestHeader(),                       // 设置header参数，使用Bearer Token方式访问资源
        data:{                                               // 传递参数
            cateId: cateId
        },
        success: function (response) {                      // 请求成功后操作
            console.log(response.data.data)
            that.setData({                                  // 为dishes页面变量赋值
                dishes: response.data.data
            })
        }
    })
  },

  // 菜系切换
  bindCateChange: function(e) {
    this.setData({
        categoryIndex: e.detail.value                       // 为categoryIndex页面变量赋值
    })
    this.getFood(this.data.categories[e.detail.value].id) // 调用getFood函数并传递菜系分类ID获取美食
  },
  // 开始和暂停按钮
  bindClickTap: function () {
    var that = this
    clearInterval(this.data.timer);  // 取消由 setInterval() 设置的 timeout
    if (this.data.isProcess) {      //  运行结束
      this.setData({
        isProcess: false,
        btnText: "开始！"
      })
      wx.showModal({
        title: '成功！',
        content: '今天就吃' + that.data.food + "！",
        confirmText: "好！",
        cancelText: "换一个",
        success: function (res) {
          if (res.confirm) {
            that.record(that.data.food) // 记录数据
            wx.navigateTo({             // 跳转页面
              url: '../choose/choose?keyword='+that.data.food
            })
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }else{                          // 开始运行
      this.setData({
        isProcess: true,
        btnText: "停！"
      })
      var newDishes = this.data.dishes
      this.data.timer = setInterval(function () {       // 按照指定的周期（以毫秒计）来调用函数
        var randomIndex = Math.floor((Math.random() * 100 % newDishes.length)) // 生成随机下标
        that.setData({
          food: newDishes[randomIndex], // 获取最终的美食
        })
      }, 10);
    }
  },
  // 记录选择的美食
  record: function (food){
    wx.request({
      url: 'http://127.0.0.1:5000/api/record/add',  // 请求URL
      data: {                                           // 请求数据
        food: food
      },
      method: 'POST',                                  // 请求方式为POST
      header: app.getRequestHeader(),                   // 设置header参数，使用Bearer Token方式访问资源
      success: function (response) {                   // 请求成功后操作
        console.log(response.msg)
      }
    })
  }
})
