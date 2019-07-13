// pages/map/map.js
var bmap = require('../../libs/bmap-wx.min.js');
Page( {
  /**
   * 页面的初始数据
   */
  data: {
    rests: [],
    food: null,
    keyword: null,
    total: 0,
    checked: false,
    pageStatus: 'loading',
  },
  bindViewTap: function (e) {
    var info = this.data.rests[e.currentTarget.id]
    console.log(info)

    wx.openLocation({
      name: info.title,
      address: info.address,
      latitude: info.latitude,
      longitude: info.longitude,
      scale: 28
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      food: options.food,
      query : options.query
    })
    var that = this;
    var BMap = new bmap.BMapWX({
      ak: '9343f3c2a6ed3c6347fd87f76af69e84'
    });
    var fail = function (data) {
      console.log(data)
    };
    var success = function (data) {
      var info = data.wxMarkerData;
      console.log(info)
      that.setData({
        rests: info,
        total: info.length,
        pageStatus: 'done'
      })
    }
    var query = this.data.keyword
    if (query == null || query === '' || query ==='undefined'){
      query = this.data.food
    }
    // 发起POI检索请求
    BMap.search({
       "query": query,
      fail: fail,
      success: success
    });
  }
})
