import os
import qrcode
import random
import time
import tkinter
from pystrich.ean13 import EAN13Encoder
import tkinter.filedialog
import tkinter.messagebox
from string import digits

root = tkinter.Tk()  # tkinter模4
# 块为python的标准图形界面接口。本代码的目的是建立根窗口
# 初始化数据
number = "1234567890"
letter = "ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890"
allis = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+"
i = 0

randstr = []
fourth = []
fifth = []
randfir = ""
randsec = ""
randthr = ""
str_one = ""
strone = ""
strtwo = ""
nextcard = ""
userput = ""
nres_letter = ""


# 创建文件夹函数
def mkdir(path):
    isexists = os.path.exists(path)  # 判断文件夹路径是否存在
    if not isexists:      # 如果文件夹路径不存在
        os.mkdir(path)     # 创建要创建的文件夹


# 读取文件内容函数
def openfile(filename):
    f = open(filename)  # 打开指定文件
    fllist = f.read()   # 读取文件内容
    f.close()           # 关闭文件
    return fllist      # 返回读取的文件内容


# 输入验证函数，showstr为input函数提供动态输入提示文字，showorder提供验证方式，length提供要求输入数据的长度
def inputbox(showstr,showorder,length):
    instr = input(showstr)  # 使用input函数要求用户输入信息，showstr为输入提示文字
    if len(instr) != 0:     # 输入数据的长度不为零
        # 根据输入数据的要求，分成三种验证方式验证，1：数字，不限位数；2：字母；3：数字且有位数要求
        if showorder == 1:  # 验证方式 ，数字格式，不限位数，大于零的整数
            if str.isdigit(instr):    # 验证是否为数字
                if instr == 0:        # 验证数字是否为0，如果是，要求重新输入，返回值为0
                    print("\033[1;31;40m 输入为零，请重新输入！！\033[0m") # 要求重新输入，返回值为“0”
                    return "0"   # 函数返回值为“0”，为什么返回值为“0”呢？读者思考一下
                else:  # 如果输入正确，返回输入的数据给返回值
                    return instr   #将输入的数据传给函数返回值
            else:      # 如果输入不是数字，要求用户重新输入，函数返回值为“0”
                print("\033[1;31;40m输入非法，请重新输入！！\033[0m")  # 要求用户重新输入
                return "0"  # 函数返回值为“0”
        if showorder == 2:  # 验证方式2 ，要求字母格式，且是三个字母
            if str.isalpha(instr): # 判断输入是否为字母
                if len(instr) != length:   # 判断输入的是否为三个字母，如果不是，则要求重新输入，返回值为“0”
                    print("\033[1;31;40m必须输入三个字母，请重新输入！！\033[0m")  # 要求重新输入
                    return "0"  # 返回值为“0”
                else:  # 如果输入是三个字母，返回输入的字母
                    return instr  # 将函数返回值设置为输入的字母
            else:  # 如果输入不是字母
                print("\033[1;31;40m输入非法，请重新输入！！\033[0m")   # 要求重新输入
                return "0"    # 返回值为“0”
        if showorder == 3:   # 验证方式3 ，要求数字格式，且输入数字位数有要求
            if str.isdigit(instr):  # 验证是否为数字
                if len(instr) != length:   # 验证输入数字是否为要求长度位数，如果不是3位数字，则要求重新输入
                    print("\033[1;31;40m必须输入" + str(length) + "个数字，请重新输入！！\033[0m") # 要求重新输入
                    return "0"  # 返回值为“0”
                else:           # 输入数字满足要求，设置函数返回值为输入信息
                    return instr  #设置函数返回值为输入信息
            else:  # 如果输入不是数字
                print("\033[1;31;40m输入非法，请重新输入！！\033[0m")  # 提示输入非法，要求重新输入
                return "0"  # 函数返回值为“0”
    else:   # 如果没有输入任何内容，即输入为空
        print("\033[1;31;40m输入为空，请重新输入！！\033[0m")   # 提示输入为空，要求重新输入
        return "0"    # 函数返回值为“0”


# 实现屏幕输出和文件输出编码信息函数，# sstr参数为输出防伪码数据, sfile为输出的文件名称
# typeis设置输出完成后是否通过信息框提示, smsg为信息提示框的提示文字，datapath 保存防伪码的文件夹
def wfile(sstr, sfile, typeis, smsg,datapath):
    mkdir(datapath)   #  调用该函数创建文件夹
    datafile = datapath + "\\" + sfile   # 设置保存防伪码的文件（包含路径）
    file = open(datafile, 'w')  # 打开保存防伪码的文件，如果文件不存在，则创建该文件
    wrlist = sstr   # 将防伪码信息赋值给wrlist
    pdata = ""      # 清空变量pdata，pdata存储屏幕输出的防伪码信息
    wdata = ""      # 清空变量 wdata ， wdata 存储保存到文本文件的防伪码信息
    for i in range(len(wrlist)):  # 按条循环读取防伪码数据
        wdata = str(wrlist[i].replace('[', '')).replace(']', '')   # 去掉字符的中括号
        wdata = wdata.replace(''''','').replace(''''', '')  # 去掉字符的引号
        file.write(str(wdata))    # 写入保存防伪码的文件
        pdata = pdata + wdata     # 将单条防伪码存储到pdata 变量
    file.close()   # 关闭文件
    print("\033[1;31m" + pdata + "\033[0m")   # 屏幕输出生成的防伪码信息
    if typeis != "no":    # 是否显示“输出完成”的信息提示框。如果typeis的值为“no”,不现显示
        # 显示“输出完成”的信息提示框。显示信息包含方位信息码的保存路径
        tkinter.messagebox.showinfo("提示", smsg + str(len(randstr)) + "\n 防伪码文件存放位置：" + datafile)
        root.withdraw()   # 关闭辅助窗口
 # 实现屏幕输出和文件输出编码信息，参数schoice设置输出的文件名称


def scode1( schoice):
    # 调用inputbox函数对输入数据进行非空、输入合法性判断
    incount = inputbox("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    while int(incount) == 0:  # 如果输入为字母或数字0,则要求重新输入
        incount = inputbox("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    randstr.clear()       # 清空保存批量注册码信息的变量randstr
    for j in range(int(incount)):   # 根据输入的验证码数量循环批量生成注册码
        randfir = ''       # 设置存储单条注册码的变量为空
        for i in range(6):  # 循环生成单条注册码
            randfir = randfir + random.choice(number)  # 产生数字随机因子　
        randfir = randfir + "\n"   # 在单条注册码后面添加转义换行字符“\n”，使验证码单条列显示　
        randstr.append(randfir)    # 将单条注册码添加到保存批量验证码的变量randstr　
    #调用函数wfile()，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr,"scode" + str(schoice) + ".txt", "", "已生成6位防伪码共计：","codepath")


# 生成9位系列产品数字防伪编码函数，参数schoice设置输出的文件名称
def scode2(schoice):
    ordstart = inputbox("\033[1;32m     请输入系列产品的数字起始号（3位）:\33[0m", 3, 3)
    while int(ordstart) == 0: # 如果输入非法（符号、字母或者数字0都认为是非法输入），重新输入
        ordstart = inputbox("\033[1;32m     请输入系列产品的数字起始号（3位）:\33[0m", 3, 3)
    ordcount = inputbox("\033[1;32m     请输入产品系列的数量:", 1, 0)
    # 如果输入的产品系列数量小于1或者大于9999,,则要求重新输入
    while int(ordcount) < 1 or int(ordcount) > 9999:
        ordcount = inputbox("\033[1;32m     请输入产品系列的数量:", 1, 0)
    incount = inputbox("\033[1;32m     请输入要生成的每个系列产品的防伪码数量:\33[0m", 1, 0)
    while int(incount) == 0:  # 如果输入为字母或数字0,则要求重新输入
        incount = inputbox("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    randstr.clear()  # 清空保存批量注册码信息的变量randstr
    for m in range(int(ordcount)):  # 分类产品编号
        for j in range(int(incount)):  # 产品防伪码编号
            randfir = ''
            for i in range(6):  # 生成一个不包含类别的产品防伪码
                randfir = randfir + random.choice(number)  # 每次生成一个随机因子
            randstr.append(str(int(ordstart) + m) + randfir + "\n") # 将生成的单条防伪码添加到防伪码列表
    #调用函数wfile()，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, "scode" + str(schoice) + ".txt", "", "已生成9位系列产品防伪码共计：","codepath")


# 生成25位混合产品序列号函数，参数schoice设置输出的文件名称
def scode3(schoice):
    # 输入要生成的防伪码数量
    incount = inputbox("\033[1;32m     请输入要生成的25位混合产品序列号数量:\33[0m", 1, 0)
    while int(incount) == 0: # 如果输入非法（符号、字母或者数字0都认为是非法输入），重新输入
        incount = inputbox("\033[1;32m     请输入要生成的25位混合产品序列号数量:\33[0m", 1, 0)
    randstr.clear()  # 清空保存批量注册码信息的变量randstr
    for j in range(int(incount)):  # 按输入数量生成防伪码
        strone = ''     # 保存生成的单条防伪码，不带横线“-”，循环时清空
        for i in range(25):
            strone = strone + random.choice(letter)   #每次产生一个随机因子，也就是每次产生单条防伪码的一位
        # 将生成的防伪码每隔5位添加横线“-”
        strtwo = strone[:5] + "-" + strone[5:10] + "-" + strone[10:15] + "-" + strone[15:20] + "-" + strone[20:25] + "\n"
        randstr.append(strtwo)   # 添加防伪码到防伪码列表
    #调用函数wfile()，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, "scode" + str(schoice) + ".txt", "", "已生成25混合防伪序列码共计：","codepath")


# 生成含数据分析功能防伪编码函数，参数schoice设置输出的文件名称
def scode4(schoice):
    intype = inputbox("\033[1;32m     请输入数据分析编号（3位字母）:\33[0m", 2, 3)
    # 验证输入是否是三个字母，所以要判断输入是否是字母和输入长度是否为3
    while not str.isalpha(intype) or len(intype) != 3:
        intype = inputbox("\033[1;32m     请输入数据分析编号（3位字母）:\33[0m", 2, 3)
    incount = inputbox("\033[1;32m     请输入要生成的带数据分析功能的验证码数量:\33[0m", 1, 0)  #
    # 验证输入是否是大于零的整数，判断输入转换为整数值时是否大于零
    while int(incount) == 0:    # 如果转换为整数时为零，则要求重新输入
        incount = inputbox("\033[1;32m     请输入要生成的带数据分析功能的验证码数量:\33[0m", 1, 0)  #
    ffcode(incount,intype,"",schoice)   # 调用 ffcode函数生成注册信息


# 生成含数据分析功能防伪编码函数，参数scount为要生成的防伪码数量，typestr为数据分析字符
# 参数ismessage在输出完成时是否显示提示信息，为“no”不显示，为其他值显示；参数schoice设置输出的文件名称
def ffcode(scount, typestr,ismessage, schoice):
    randstr.clear()  # 清空保存批量注册码信息的变量randstr
    # 按数量生成含数据分析功能注册码
    for j in range(int(scount)):
        strpro = typestr[0].upper()    # 取得三个字母中的第一个字母，并转为大写，区域分析码
        strtype = typestr[1].upper()   # 取得三个字母中的第二个字母，并转为大写，颜色分析码
        strclass = typestr[2].upper()  # 取得三个字母中的第三个字母，并转为大写，版本分析码
        randfir = random.sample(number, 3)  # 随机抽取防伪码中的三个位置，不分先后
        randsec = sorted(randfir)  # 对抽取的位置进行排序并存储给randsec变量，以便按顺序排列三个字母的位置
        letterone = ""    # 清空存储单条防伪码的变量letterone
        for i in range(9):  # 生成9位的数字防伪码
            letterone = letterone + random.choice(number)
        # 将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量中
        sim = str(letterone[0:int(randsec[0])]) + strpro + str(
            letterone[int(randsec[0]):int(randsec[1])]) + strtype + str(
            letterone[int(randsec[1]):int(randsec[2])]) + strclass + str(letterone[int(randsec[2]):9]) + "\n"
        randstr.append(sim)   # 将组合生成的新防伪码添加到randstr变量
    # 调用wfile()函数，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, typestr + "scode" + str(schoice) + ".txt", ismessage, "生成含数据分析防伪码共计：","codepath")


# 生成含数据分析功能防伪编码函数，参数schoice设置输出的文件名称
def scode5(schoice):
    default_dir = r"mrsoft.mri"    # 设置默认打开的文件名称

    # 打开文件选择对话框，指定打开的文件名称为"mrsoft.mri" ，扩展名为“mri”，可以使用记事本打开和编辑
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Text file","*.mri")],title=u"请选择自动防伪码智能批处理文件：",
                                                   initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)   # 读取从文件选择对话框选中的文件
    print("前：",codelist)
    codelist = codelist.split("\n")  # 把读取的信息内容添加回车，以便列输出显示
    print("后：",codelist)
    for item in codelist:           # 按读取的信息循环生成防伪码
        codea = item.split(",")[0]   # 每一行信息中用 ","分割，","前面的信息存储防伪码标准信息
        codeb = item.split(",")[1]   # 每一行信息中用 ","分割，","后面的信息存储防伪码生成的数量
        ffcode(codeb, codea,"no" ,schoice)  # 调用ffcode函数批量生成同一标识信息的防伪码


#  后续补加生成防伪码函数，防伪码格式为带数据分析功能注册码
def scode6(schoice):
    default_dir = r"c:\ABDscode5.txt"    # 设置默认打开的文件名称
    # 按默认的文件名称打开文件选择对话框，用于打开已经存在的防伪码文件
    file_path = tkinter.filedialog.askopenfilename(title=u"请选择已经生成的防伪码文件",initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)      # 读取从文件选择对话框选中的文件
    codelist = codelist.split("\n")     #  把读取的信息内容添加回车，以便列输出显示
    codelist.remove("")                 # 删除列表中的空行
    strset = codelist[0]                # 读取一行数据，以便获取原验证码的字母标志信息
    remove_digits = strset.maketrans("", "", digits)  # 用maketrans方法创建删除数字的字符映射转换表
    res_letter = strset.translate(remove_digits)  # 根据字符映射转换表删除该条防伪码中的数字，获取字母标识信息
    nres_letter = list(res_letter)   # 把信息用列表变量nres_letter存储
    strpro = nres_letter[0]    # 从列表变量中取得第一个字母，即区域分析码
    strtype = nres_letter[1]   # 从列表变量中取得第二个字母，即色彩分析码
    strclass = nres_letter[2]   # 从列表变量中取得第三个字母，即版次分析码
    # 去除信息中的括号和引号
    nres_letter = strpro.replace(''''','').replace(''''', '') + strtype.replace(
        ''''','').replace(''''', '') + strclass.replace(''''','').replace(''''', '')
    print("sssssssssss",nres_letter)
    card = set(codelist)   # 将原有防伪码放到集合变量card中
    # 利用tkinter的messagebox提示用户之前生成的防伪码数量
    tkinter.messagebox.showinfo("提示", "之前的防伪码共计：" + str(len(card)))
    root.withdraw() # 关闭提示信息框
    incount = inputbox("请输入补充验证码生成的数量:", 1, 0)  # 让用户输入新补充生成的防伪码数量
    # 最大值按输入生成数量的2倍数量生成新防伪码，防止新生成防伪码与原有防伪码重复造成新生成的防伪码数量不够,
    for j in range(int(incount) * 2):
        randfir = random.sample(number, 3)   # 随机产生3位不重复的数字
        randsec = sorted(randfir)            #对产生的数字排序
        addcount = len(card)                  # 记录集合中防伪码的总数量
        strone = ""                           # 清空存储单条防伪码的变量strone
        for i in range(9):                    # 生成9位的数字防伪码
            strone = strone + random.choice(number)
         # 将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量中
        sim = str(strone[0:int(randsec[0])]) + strpro + str(
            strone[int(randsec[0]):int(randsec[1])]) + strtype + str(
            strone[int(randsec[1]):int(randsec[2])]) + strclass + str(strone[int(randsec[2]):9]) + "\n"
        card.add(sim)  # 添加新生成的防伪码到集合
        # 如果添加到集合,证明生成的防伪码与原有的防伪码没有产生重复
        if len(card) > addcount:
            randstr.append(sim)   # 添加新生成的防伪码到新防伪码列表
            addcount = len(card)  # 记录最添加新生成防伪码集合的防伪码数量
        if len(randstr) >= int(incount):   # 如果新防伪码列表中的防伪码数量达到输入的防伪码数量
            print(len(randstr))            # 输出已生成防伪码的数量
            break                          # 退出循环
    # 调用函数wfile()函数，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, nres_letter + "ncode" + str(choice) + ".txt", nres_letter, "生成后补防伪码共计：","codeadd")
    # tkinter.messagebox.showinfo("提示", "已生成补充防伪码共：" + str(len(randstr)))    # 提示
    # root.withdraw()


#  条形码EAN13批量生成函数
def scode7(schoice):
    mainid = inputbox("\033[1;32m     请输入EN13的国家代码（3位） :\33[0m", 3, 3)  # 输入3位国家代码
    # while int(mainid) < 1 or len(mainid) != 3:   # 验证输入是否为3位数字（转为整数后小于1和长度不等于3，重新输入）
    #     mainid = inputbox("\033[1;32m     请输入EAN13的国家代码（3位）::\33[0m", 1, 0)
    compid = inputbox("\033[1;32m     请输入EAN13的企业代码（4位）:\33[0m", 3, 4)  # 输入4位企业代码
    # while int(compid) < 1 or len(compid) != 4:   # 验证输入是否为4位数字
    #     compid = inputbox("\033[1;32m     请输入EAN13的企业代码（4位）:\33[0m", 1, 0)
    incount = inputbox("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)   # 输入要生成的条形码数量
    while int(incount) == 0:   # 输入信息转为整数后等于0，重新输入
        incount = inputbox("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)
    mkdir("barcode")  # 判断保存条形码的文件夹是否存在，不存在，则创建该文件夹
    for j in range(int(incount)):   # 批量生成条形码
        strone = ''  # 清空存储单条条形码的变量
        for i in range(5):  # 生成条形码的6位（除国家代码、企业代码和校验位之外的6位）数字
            strone = strone + str(random.choice(number))
        barcode=mainid +compid +strone   # 把国家代码、企业代码和新生成的随机码进行组合
        # 计算条形码的校验位
        evensum = int(barcode[1])  + int(barcode[3])  + int(barcode[5]) + int(barcode[7])  + int(barcode[9])  +int(barcode[11]) # 偶数位
        oddsum =int( barcode[0])+int(barcode[2])+int(barcode[4])+int(barcode[6])+int(barcode[8]) +int(barcode[10])
        # checkbit=int(10-(evensum *3 + oddsum)%10)
        checkbit = int((10 - (evensum * 3 + oddsum) %10)% 10)
        barcode=barcode+str(checkbit)  # 组成完整的EAN13条形码的13位数字
        print (barcode)
        encoder = EAN13Encoder(barcode)  # 调用EAN13Encoder生成条形码
        encoder.save("barcode\\" + barcode  + ".png")  # 保存条形码信息图片到文件


# 本函数生成固定的12位二维码，读者可以根据实际需要修改成按输入位数进行生成的函数
def scode8(schoice):
     # 输入要生成的二维码数量
     incount = inputbox("\033[1;32m     请输入要生成的12位数字二维码数量:\33[0m", 1, 0)
     while int(incount) == 0:  # 如果输入不是大于0的数字，重新输入
        incount = inputbox("\033[1;32m     请输入要生成的12位数字二维码数量:\33[0m", 1, 0)
     mkdir("qrcode")     # 判断保存二维码的文件夹是否存在，不存在，则创建该文件夹
     for j in range(int(incount)):    # 批量生成二维码
        strone = ''   # 清空存储单条二维码的变量
        for i in range(12):  # 生成单条二维码数字
            strone = strone + str(random.choice(number))
        encoder =qrcode.make(strone)  # 生成二维码
        encoder.save("qrcode\\" + strone  + ".png") # 保存二维码图片到文件


#抽奖函数
def scode9(schoice):
   default_dir = r"lottery.ini"    # 设置默认打开文件为开发路径下的"lottery.ini"
   # 选择包含用户抽奖信息票号的文件，扩展名为“*.ini”
   file_path = tkinter.filedialog.askopenfilename(filetypes=[("Ini file","*.ini")],title=u"请选择包含抽奖号码的抽奖文件：",initialdir=(os.path.expanduser(default_dir)))
   codelist = openfile(file_path)  # 调用 openfile()函数读取刚打开的抽奖文件
   codelist = codelist.split("\n")   # 通过回行转义符把抽奖信息分割成抽奖数列
   incount = inputbox("\033[1;32m     请输入要生成的中奖数量:\33[0m", 1, 0)  # 要求用户输入中（抽）奖数量
   while int(incount) == 0  or len(codelist)< int(incount):   # 如果输入中（抽）奖数量等于0或超过抽奖数组数量，重新输入
       incount = inputbox("\033[1;32m     请输入要生成的抽奖数量:\33[0m", 1, 0)
   strone = random.sample(codelist,int(incount))  # 根据输入的中奖数量进行抽奖

   print("\033[1;35m     抽奖信息名单发布：   \33[0m")
   for i in range(int(incount)):  # 循环将抽奖数列的引号和中括号去掉
       wdata = str(strone[i].replace('[', '')).replace(']', '') # 将抽奖数列的中括号去掉
       wdata = wdata.replace(''''','').replace(''''', '')  # 将抽奖数列的引号去掉
       print("\033[1;32m         " +  wdata  + "\33[0m")      # 输出中奖信息


# 输入数字验证，判断输入是否在0-9之间的整数
def input_validation(insel):
    if str.isdigit(insel):
        insel = int(insel)
        # if insel == 0:
        #     # print("\033[1;31;40m    输入非法，请重新输入！！\033[0m")
        #     return 0
        # else:
        #     return insel
        return insel
    else:
        print("\033[1;31;40m       输入非法，请重新输入！！\033[0m")
        return 0

# 企业编码管理系统主菜单
def mainmenu():
    # os.system("clear")
    print("""\033[1;35m
      ****************************************************************
                            企业编码生成系统
      ****************************************************************
          1.生成6位数字防伪编码 （213563型）
          2.生成9位系列产品数字防伪编码(879-335439型)
          3.生成25位混合产品序列号(B2R12-N7TE8-9IET2-FE35O-DW2K4型)
          4.生成含数据分析功能的防伪编码(5A61M0583D2)
          5.智能批量生成带数据分析功能的防伪码
          6.后续补加生成防伪码(5A61M0583D2)
          7.EAN-13条形码批量生成
          8.二维码批量输出          
          9.企业粉丝防伪码抽奖
          0.退出系统
      ================================================================
      说明：通过数字键选择菜单
      ================================================================
    \033[0m""")


def codeprint(cstr, cint):
    str1 = cstr[0]
    str2 = cstr[1]
    str3 = cstr[2]
    for i in range(int(cint)):
        strbook = str1 + str2 + random.choice(letter) + random.choice(letter) + random.choice(letter) + str2 + str3
        print(strbook)


# 通过循环控制用户对程序功能的选择
while i < 9:
    # 调入程序主界面菜单
    mainmenu()
    # 键盘输入需要操作的选项
    choice = input("\033[1;32m     请输入您要操作的菜单选项:\33[0m")
    if len(choice) != 0:  # 输入如果不为空
        choice = input_validation(choice)  # 验证输入是否为数字
        if choice == 1:
           scode1( str(choice))      # 如果输入大于零的整数，调用scode1()函数生成注册码
        # 选择菜单2,调用scode2()函数生成9位系列产品数字防伪编码
        if choice == 2:
            scode2(choice)
        # 选择菜单3,调用scode3()函数生成25位混合产品序列号
        if choice == 3:
            scode3(choice)
        # 选择菜单4,调用scode4()函数生成含数据分析功能的防伪编码
        if choice == 4:
            scode4(choice)
        # 选择菜单5,调用scode5()函数智能批量生成带数据分析功能的防伪码
        if choice == 5:
            scode5(choice)
        # 选择菜单６,调用scode6()函数后续补加生成防伪码
        if choice == 6:
            scode6(choice)
        # 选择菜单7,调用scode7()函数批量生成条形码
        if choice == 7:
          scode7( choice)
        # 选择菜单8,调用scode8()函数批量生成二维码
        if choice == 8:
            scode8( choice)
        # 选择菜单9,调用scode9()函数生成企业粉丝抽奖程序
        if choice == 9:
            scode9( choice)
        # 选择菜单0,退出系统
        if choice == 0:
            i = 0
            print("正在退出系统!!")
            break
    else:
        print("\033[1;31;40m    输入非法，请重新输入！！\033[0m")
        time.sleep(2)
