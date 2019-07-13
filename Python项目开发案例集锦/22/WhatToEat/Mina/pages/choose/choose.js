Page({
  data: {
    food : null
  },
  onLoad: function(option){
    console.log(option.keyword)
    this.setData({
      food: option.keyword,
    })
  }
})