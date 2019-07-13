// pages/login.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.setNavigationBarTitle({
        title: '今天吃什么？'
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
        var that = this;
        setTimeout(function () {
            that.setData({
                remind: ''
            });
        }, 1000);
        // 实现动画效果
        wx.onAccelerometerChange(function (res) {
            var angle = -(res.x * 30).toFixed(1);
            if (angle > 14) {
                angle = 14;
            }
            else if (angle < -14) {
                angle = -14;
            }
            if (that.data.angle !== angle) {
                that.setData({
                    angle: angle
                });
            }
        });
  },

  // 跳转到首页方法
  goToIndex: function () {
    wx.switchTab({
        url: '/pages/index/index',
    });
  },
  // 登录方法
  login:function( e ){
    var that = this;
    if( !e.detail.userInfo ){
        app.alert( { 'content':'登录失败，请再次点击' } );
        return;
    }
    var data = e.detail.userInfo;
    wx.login({
        success:function( res ){
            if( !res.code ){
                wx.showToast({
                  title: '提示信息',
                  icon: '登录失败，请再次点击'
                });
                return;
            }
            // 发送请求，获取用户信息
            wx.request({
                url:'http://127.0.0.1:5000/api/user/login' ,     // 请求URL
                header:app.getRequestHeader(),                        // 请求header信息
                method:'POST',                                       // 请求方式
                data: {'code': res.code},                             // 请求数据,传递code
                success:function( res ){                             // 请求成功后操作
                    if( res.data.code != 200 ){
                        wx.showToast({
                          title: res.data.msg,
                          icon: 'none'
                        });
                        return;
                    }
                    app.globalData.userInfo = res.data.data.userInfo; // 写入全局变量
                    // 为页面变量赋值
                    that.setData({
                        userInfo: res.data.data.userInfo,
                    })
                    app.setCache( 'token',res.data.data.token );  // 写入缓存
                    that.goToIndex();                              // 跳转到首页
                }
            });
        }
    });
  }
})