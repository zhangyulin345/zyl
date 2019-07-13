from PIL import Image,ImageDraw,ImageFont # 导入图像处理模块(图像、图像绘制、图像文字)
import numpy     # 导入numpy模块，用于创建数组对象


scale = 1  # 生成后图片的缩放比例
default_char ='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft我爱Python' # 默认字符

"""
该方法用于实现字符画图片的转换与生成
import_img：该参数为指定原图片的路径
export_img：该参数为转换后字符画图片输出路径
input_char：该参数为自定义字符画中的字符内容，如果该参数为空将使用默认参数
pix_distance：该参数为字符画图片的字符密度，3为清晰，4为一般，5为字符
"""
def picture_conversion(import_img, export_img = None,input_char = '',pix_distance=''):
    # 导入图片处理
    img = Image.open(import_img)     #读取图片信息
    img_pix = img.load()                        # 加载图片像素
    img_width = img.size[0]                     # 获取图片宽度
    img_height = img.size[1]                    # 获取图片高度

    #创建新图片画布
    canvas_array = numpy.ndarray((img_height*scale, img_width*scale, 3), numpy.uint8)  # 创建画布数组对象
    canvas_array[:, :, :] = 255                                    # 设置画布的三元色(255 255 255)为白色
    new_image = Image.fromarray(canvas_array)                      # 根据画布创建新的图像
    img_draw = ImageDraw.Draw(new_image)                               # 创建图像绘制对象
    font = ImageFont.truetype('simsun.ttc', 10)                        # 字库类型

    # 判断字符画所使用的字符
    if input_char=='':
        char_list = list(default_char)                                 # 指定默认显示的字符列表
    else:
        char_list =list(input_char)

    # 判断选择的清晰度
    if pix_distance=='清晰':
        pix_distance=3
    elif pix_distance=='一般':
        pix_distance=4
    elif pix_distance=='字符':
        pix_distance=5

    #开始绘制
    pix_count = 0                                   # 记录绘制的字符像素点数量
    table_len = len(char_list)                      # 字符长度
    for y in range(img_height):                     # 根据图片高度，获取y坐标
        for x in range(img_width):                  # 根据图片宽度，获取x坐标
            if x % pix_distance == 0 and y % pix_distance == 0:   # 判断字符间隔位置
                # 实现根据图片像素绘制字符
                img_draw.text((x*scale, y*scale), char_list[pix_count % table_len], img_pix[x, y], font)
                pix_count += 1                   # 叠加绘制字符像素点数量

    # 保存
    if export_img is not None:    # 判断如果设置了新图片保存的名称与路径
        new_image.save(export_img) # 实现字符图片的保存
    return False   # 通知说明已经转换完毕



