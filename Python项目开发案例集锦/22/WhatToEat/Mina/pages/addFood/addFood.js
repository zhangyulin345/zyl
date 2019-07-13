const app = getApp()
Page({
  data: {
    userInfo: {},
    categories: [],
    categoryIndex: 0,
    food: ''
  },

  onShow: function (){
    // 判断是否登录
    var that = this
    wx.checkSession({
      success: function () {
        //session_key 未过期，并且在本生命周期一直有效
        that.setData({
            categories: app.getCache('categories')
        });
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

  // 菜系切换
  bindCateChange: function(e) {
    this.setData({
        categoryIndex: e.detail.value
    })
  },
  // 提交表单
  formSubmit: function(e) {
    var that = this
    var categories = wx.getStorageSync('categories')
    var categoryIndex = e.detail.value.categoryIndex
    var cate_id = categories[categoryIndex].id
    var food = e.detail.value.food
    if (!food){
        wx.showToast({
          title: '请填写美食名称',
          icon: 'none'
        });
        return false;
    }
    wx.request({
      url: 'http://127.0.0.1:5000/api/food/foodAdd',
      data: {
        cate_id: cate_id,
        food: food
      },
      method: 'POST',
      header: app.getRequestHeader(),
      success: function (response) {
        if (response.data.code == 200){
            var icon = 'success'
            that.setData({
                food: ''
            })
        }else {
            var icon = 'none'
        }
        wx.showToast({
          title: response.data.msg,
          icon: icon
        });
      },
      fail: function () {
        wx.showToast({
          title: '网络繁忙，稍后再试',
          icon: 'none'
        });
      },
      complete: function () {
        wx.hideLoading();
      }
    });
  }
})
