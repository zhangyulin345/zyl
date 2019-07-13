# -*- coding: utf-8 -*-
'''
   合并pdf文件，输出的pdf文件按输入的pdf文件名生成书签
'''
import os, sys, codecs
from PyPDF2 import PdfFileReader, PdfFileMerger
import tools.common as common

def mergefiles(path, output_filename, import_bookmarks=False):
    ''' 遍历目录下的所有pdf将其合并输出到一个pdf文件中， # 返回数字（将按该数字排序）输出的pdf文件默认带书签，
    书签名为之前的文件名。默认情况下原始文件的书签不会导入，使用import_bookmarks=True可以将原文件所带的书签也
    导入到输出的PDF文件中
    '''
    merger = PdfFileMerger()
    filelist = common.getfilenames(filepath=path,filelist_out=[], file_ext='.pdf')  # 获取要合并的PDF文件
    if len(filelist) == 0:
        print("当前目录及子目录下不存在pdf文件")
        sys.exit()
    for filename in filelist:
        f = codecs.open(filename, 'rb') # 使用codecs的open()方法打开文件时，会自动转换为内部Unicode编码
        file_rd = PdfFileReader(f)
        short_filename = os.path.basename(os.path.splitext(filename)[0])
        if file_rd.isEncrypted == True:
            print('不支持的加密文件：%s'%(filename))
            continue
        merger.append(file_rd, bookmark=short_filename, import_bookmarks=import_bookmarks)
        f.close()  # 关闭文件对象
    out_filename=os.path.join(os.path.abspath(path), output_filename)  # 将文件名和路径连接为一个完整路径
    merger.write(out_filename)
    merger.close()
# 测试用的代码
# if __name__ == "__main__":
#     mergefiles(r'E:\learn\test\pdf','merged.pdf',True)
