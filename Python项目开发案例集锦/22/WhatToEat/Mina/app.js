//app.js
App({
  globalData: {
    userInfo: null
  },
  getRequestHeader:function(){
    return {
        'content-type': 'application/x-www-form-urlencoded',
        "Authorization": "Bearer " + wx.getStorageSync('token')
    }
  },
  getCache:function( key ){
    var value = undefined;
    try {
        value = wx.getStorageSync( key );
    } catch (e) {
    }
    return value;
  },
  setCache:function(key,value){
    wx.setStorage({
         key:key,
        data:value
    });
  },
})