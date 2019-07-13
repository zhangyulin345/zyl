const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    id: null,
    info:[],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (option) {
    this.setData({
        id: option.id,
    })
    this.getCookDetail(option.id)
  },
  /**
  * 获取菜谱详细信息
  */
  getCookDetail: function (id) {
    var that = this
    wx.request({
        url: 'http://127.0.0.1:5000/api/food/cookDetail',
        header: app.getRequestHeader(),
        method: "POST",
        data: {'id': id},
        success: function(response){
            console.log(response.data.data)
            that.setData({
                info: response.data.data
            })
        }
    })
  },
  /**
  * 图片点击事件
  */
 imgYu:function(event){
     var src = event.currentTarget.dataset.src;//获取data-src
     var imgList = event.currentTarget.dataset.list;//获取data-list
     //图片预览
     wx.previewImage({
      current: src, // 当前显示图片的http链接
      urls: imgList // 需要预览的图片http链接列表
     })
 }
})
