//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false
  },
  onLoad: function () {
    if (app.globalData.userInfo == null) {
      this.bindLogin();
    }
  },
  onShow: function(){
    this.setData({
      userInfo: app.globalData.userInfo
    });
  },
  //开始游戏
  bindBegin: function () {
    var that = this;
    if (this.data.userInfo.sesion >= app.globalData.sesionTotal) {
      wx.navigateTo({
        url: '../success/success'
      });
    } else {
      wx.navigateTo({
        url: '../guess/guess'
      });
    }
  },
  // 用户登录
  bindLogin: function (e) {
    var that = this;
    // 微信登录
    wx.login({
      success: function (loginRes) {
        if (loginRes.code) {
          // 查看是否授权
          wx.getSetting({
            success: function (res) {
              if (res.authSetting['scope.userInfo']) {
                // 微信获取用户信息
                wx.getUserInfo({
                  success: function (result) {
                    console.log("已获取到用户信息");
                    // 执行登录
                    that.wxlogin(loginRes.code,result.userInfo.nickname,result.userInfo.avatar)
                  }
                });
              } else {
                wx.showToast({
                  title: '请先授权用户信息',
                  icon: "none"
                });
              }
            }
          });
        }
      }
    });
  },
  // 服务器登录
  wxlogin: function (code,nickname,avatar) {
    var that = this;
    wx.showLoading({
      title: '正在登录中',
      mask: true
    });
    wx.request({
      url: 'http://127.0.0.1:5000/api/users/wx_login',
      data: {
        code: code,
        nickname:nickname,
        avatar:avatar,
      },
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (response) {
        var userInfo = response.data.data.userInfo;
        var sesionTotal = response.data.data.sesionTotal;
        var token = response.data.data.token;
        console.log(response)
        // 将token写入缓存
        try {
          wx.setStorageSync('token', token)
        } catch (e) {
          console.log('storage token error')
        }
        app.globalData.sesionTotal = sesionTotal;
        if (userInfo.userId > 0) {
          app.globalData.userInfo = userInfo;
          that.setData({
            userInfo: userInfo,
            hasUserInfo: true
          });
        }
      },
      fail: function () {
        console.log("wxlogin fail");
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        });
      },
      complete: function () {
        wx.hideLoading();
      }
    });
  },
  // 查看排行榜
  bindRank: function(){
    wx.navigateTo({
      url: '../rank/rank'
    });
  }
})
