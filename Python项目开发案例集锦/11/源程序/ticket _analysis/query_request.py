import requests

from get_stations import *
import json  # 导入json模块

'''5-7 目的地 3  车次 6  出发地 8  出发时间 9  到达时间 10 历时 26 无坐 29 硬座
   24 软座 28 硬卧 33 动卧 23 软卧 21 高级软卧 30 二等座 31 一等座 32 商务座特等座
'''
data = []  # 用于保存整理好的车次信息
type_data = []  # 保存车次分类后最后的数据


def query(date, from_station, to_station):
    data.clear()  # 清空数据
    type_data.clear()  # 清空车次分类保存的数据
    # 查询请求地址
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    # 发送查询请求
    response = requests.get(url)
    # # 将json数据转换为字典类型，通过键值对取数据
    result = response.json()
    result = result['data']['result']
    # 判断车站文件是否存在
    if is_stations('stations.text') == True:
        stations = eval(read('stations.text'))  # 读取所有车站并转换为dic类型
        if len(result) != 0:  # 判断返回数据是否为空
            for i in result:
                # # 分割数据并添加到列表中
                tmp_list = i.split('|')
                # 因为查询结果中出发站和到达站为站名的缩写字母，所以需要在车站库中找到对应的车站名称
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
                # 创建座位数组，由于返回的座位数据中含有空既“”，所以将空改成--这样好识别
                seat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10]
                    , tmp_list[32], tmp_list[31], tmp_list[30], tmp_list[21]
                    , tmp_list[23], tmp_list[33], tmp_list[28], tmp_list[24], tmp_list[29], tmp_list[26]]
                newSeat = []
                # 循环将座位信息中的空既“”，改成--这样好识别
                for s in seat:
                    if s == "":
                        s = "--"
                    else:
                        s = s
                    newSeat.append(s)  # 保存新的座位信息
                data.append(newSeat)
        return data  # 返回整理好的车次信息


# 获取高铁信息的方法
def g_vehicle():
    if len(data) != 0:
        for g in data:  # 循环所有火车数据
            i = g[0].startswith('G')  # 判断车次首字母是不是高铁
            if i:  # 如果是将该条信息添加到高铁数据中
                type_data.append(g)


# 移除高铁信息的方法
def r_g_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith('G')
            if i:  # 移除高铁信息
                type_data.remove(g)


# 获取动车信息的方法
def d_vehicle():
    if len(data) != 0:
        for d in data:  # 循环所有火车数据
            i = d[0].startswith('D')  # 判断车次首字母是不是动车
            if i == True:  # 如果是将该条信息添加到动车数据中
                type_data.append(d)


# 移除动车信息的方法
def r_d_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for d in data:
            i = d[0].startswith('D')
            if i == True:  # 移除动车信息
                type_data.remove(d)


# 获取直达车信息的方法
def z_vehicle():
    if len(data) != 0:
        for z in data:  # 循环所有火车数据
            i = z[0].startswith('Z')  # 判断车次首字母是不是直达
            if i == True:  # 如果是将该条信息添加到直达数据中
                type_data.append(z)


# 移除直达车信息的方法
def r_z_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for z in data:
            i = z[0].startswith('Z')
            if i == True:  # 移除直达车信息
                type_data.remove(z)


# 获取特快车信息的方法
def t_vehicle():
    if len(data) != 0:
        for t in data:  # 循环所有火车数据
            i = t[0].startswith('T')  # 判断车次首字母是不是特快
            if i == True:  # 如果是将该条信息添加到特快车数据中
                type_data.append(t)


# 移除特快车信息的方法
def r_t_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for t in data:
            i = t[0].startswith('T')
            if i == True:  # 移除特快车信息
                type_data.remove(t)


# 获取快速车数据的方法
def k_vehicle():
    if len(data) != 0:
        for k in data:  # 循环所有火车数据
            i = k[0].startswith('K')  # 判断车次首字母是不是快车
            if i == True:  # 如果是将该条信息添加到快车数据中
                type_data.append(k)


# 移除快速车数据的方法
def r_k_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for k in data:
            i = k[0].startswith('K')
            if i == True:  # 移除快车信息
                type_data.remove(k)




'''5-7 目的地 3  车次 6  出发地 8  出发时间 9  到达时间 10 历时 26 无坐 29 硬座
   24 软座 28 硬卧 33 动卧 23 软卧 21 高级软卧 30 二等座 31 一等座 32 商务座特等座
'''

today_car_list = []  # 保存今天列车信息，已经处理是否有票
three_car_list = []  # 保存三天列车信息，已经处理是否有票
five_car_list = []  # 保存五天列车信息，已经处理是否有票

today_list=[]       # 保存今天列车信息，未处理
three_list = []  # 保存三天列车信息，未处理是否有票
five_list = []  # 保存五天列车信息，未处理是否有票


# 查询卧铺售票分析数据
def query_ticketing_analysis(date, from_station, to_station, which_day):
    # 查询请求地址
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    # 发送查询请求
    response = requests.get(url)
    # 将json数据转换为字典类型，通过键值对取数据
    result = response.json()
    result = result['data']['result']
    # 判断车站文件是否存在
    if is_stations('stations.text') == True:
        stations = eval(read('stations.text'))  # 读取所有车站并转换为dic类型
        if len(result) != 0:  # 判断返回数据是否为空
            for i in result:
                # # 分割数据并添加到列表中
                tmp_list = i.split('|')
                # 因为查询结果中出发站和到达站为站名的缩写字母，所以需要在车站库中找到对应的车站名称
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
                # 创建座位数组，其中包含高级软卧、软卧、硬卧
                seat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10]
                    , tmp_list[21], tmp_list[23], tmp_list[28]]
                if which_day == 1:  # 判断今天的车次信息
                    # 将高铁、动、C开头的车次，排除
                    if seat[0].startswith('G') == False and seat[0].startswith('D') == False and seat[
                        0].startswith('C') == False:
                        today_list.append(seat)    # 将高级软卧、软卧、硬卧未处理信息添加至列表中
                        new_seat = is_ticket(tmp_list,from_station,to_station) # 判断某车次是否有票
                        today_car_list.append(new_seat)  # 将判断后的车次信息添加至对应的列表当中
                if which_day == 3:  # 判断三天的车次信息
                    # 将高铁、动、C开头的车次，排除
                    if seat[0].startswith('G') == False and seat[0].startswith('D') == False and seat[
                        0].startswith('C') == False:
                        three_list.append(seat)  # 将高级软卧、软卧、硬卧未处理信息添加至列表中
                        new_seat = is_ticket(tmp_list, from_station, to_station)  # 判断某车次是否有票
                        three_car_list.append(new_seat)  # 将判断后的车次信息添加至对应的列表当中
                if which_day == 5:  # 判断五天的车次信息
                    # 将高铁、动、C开头的车次，排除
                    if seat[0].startswith('G') == False and seat[0].startswith('D') == False and seat[
                        0].startswith('C') == False:
                        five_list.append(seat)  # 将高级软卧、软卧、硬卧未处理信息添加至列表中
                        new_seat = is_ticket(tmp_list, from_station, to_station)  # 判断某车次是否有票
                        five_car_list.append(new_seat)  # 将判断后的车次信息添加至对应的列表当中

# 判断高级软卧、软卧、硬卧是否有票
def is_ticket(tmp_list,from_station, to_station):
    # 判断高级软卧、软卧、硬卧任何一个有票的话，就说明该趟类车有卧铺车票
    if tmp_list[21]=='有' or tmp_list[23]=='有' or tmp_list[28]=='有':
        tmp_tem = '有'
    else:
        # 判断高级软卧、软卧、硬卧对应的如果是数字说明也有票，其它为无票
        if tmp_list[21].isdigit() or tmp_list[23].isdigit() or tmp_list[28].isdigit():
            tmp_tem = '有'
        else:
            tmp_tem = '无'

    # 创建新的座位列表，显示某趟列车是否有卧铺票
    new_seat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10]
        ,tmp_tem ]
    return new_seat # 返回该列表


station_name_list = []  # 保存起售车站名称列表
station_time_list = []  # 保存起售车站对应时间列表


def query_time(station):
    station_name_list.clear()  # 清空数据
    station_time_list.clear()  # 清空数据
    stations = eval(read('time.text'))  # 读取所有车站并转换为dic类型
    url = 'https://www.12306.cn/index/otn/index12306/queryScSname'  # 请求地址
    form_data = {"station_telecode": station}  # 表单参数，station参数为需要搜索车站的英文缩写
    response = requests.post(url, data=form_data, verify=True)  # 请求并进行验证
    response.encoding = 'utf-8'  # 对请求所返回的数据进行编码
    json_data = json.loads(response.text)  # 解析json数据
    data = json_data.get('data')  # 获取json中可用数据，也就是查询车站所对应的站名
    for i in data:  # 遍历查询车站所对应的所有站名
        if i in stations:  # 在站名时间文件中，判断是否存在该站名
            station_name_list.append(i)  # 有该站名就将站名添加至列表中
    for name in station_name_list:  # 遍历筛选后的站名
        time = stations.get(name)  # 通过站名获取对应的时间
        station_time_list.append(time)  # 将时间保存至列表
    return station_name_list, station_time_list # 将列表信息返回

