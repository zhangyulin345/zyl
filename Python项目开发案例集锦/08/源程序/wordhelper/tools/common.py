import os  # 导入系统功能模块

# 指定排序规则
import re
def indexSort(elem):
    a = re.findall(r"第\d*章",elem)
    if a == []:  # 不存在数字时
        return float("inf") # 返回一个正无穷的数，表示最大
    else:
        return int(a[0][1:-1])

'''获取指定目录下的文件
   filepath：要遍历的目录
   filelist_out：输出文件列表
   file_ext：文件的扩展名，默认为任何类型的文件
'''
def getfilenames(filepath='',filelist_out=[],file_ext='all'):
    # 遍历filepath下的文件
    for filename in os.listdir(filepath):
        fi_d = os.path.join(filepath, filename)
        if file_ext == '.doc':  # 遍历Word文档文件
            if os.path.splitext(fi_d)[1] in ['.doc','.docx']:
                filelist_out.append(fi_d) # 添加到路径列表中
        else:
            if  file_ext == 'all':  # 遍历全部文件
                filelist_out.append(fi_d) # 添加到路径列表中
            elif os.path.splitext(fi_d)[1] == file_ext:
                filelist_out.append(fi_d)  # 添加到路径列表中
            else:
                pass
    filelist_out.sort(key=indexSort)  # 对列表进行排序
    return filelist_out  # 返回文件完整路径列表
