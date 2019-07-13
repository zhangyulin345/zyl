// pages/test/test.js
Page({

  /**
   * 页面的初始数据
   */
    data: {
        Data: [{id:0,name:'A' },{id:5,name:'B' }],
        Index: 0,
        currentId : 0
    },
  bindChange: function(e) {
    this.setData({
        Index: e.detail.value
    })
    console.log(e.detail.value)
    console.log(this.data.Data[e.detail.value].id)

  },
})