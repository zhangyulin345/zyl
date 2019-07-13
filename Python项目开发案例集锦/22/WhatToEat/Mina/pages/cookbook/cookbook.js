const app = getApp()
Page({
    data:{
        pageStatus: 'loading',  // 加载标识
        food : null,            //  美食名称
        cookbook : []            //  菜谱列表
    },
    onLoad: function(option){
        this.setData({
          food: option.food,             // 为页面变量赋值
        })
        this.getCookBook(option.food)   // 调用获取菜谱方法
    },
    // 获取菜谱列表
    getCookBook: function(food){
        this.setData({pageStatus: 'loading'})
        var that = this
        wx.request({
            url: 'http://127.0.0.1:5000/api/food/cookbook',  // 请求URL
            method: 'POST',                                        // 请求方式为POST
            header: app.getRequestHeader(),                         //  设置header参数，使用Bearer Token方式访问资源
            data: {'food':food},                                    // 请求成功后操作
            success: function (response) {
                console.log(response.data.data)
                that.setData({
                    cookbook: response.data.data,                  // 设置菜谱数据
                    pageStatus: 'done'                             // 更改加载标识
                })
            }
        })
    },
    // 跳转首页方法
    goToIndex: function (){
        wx.switchTab({
            url: "../index/index"
        });
    }
})
