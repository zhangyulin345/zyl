#-*- coding=UTF-8 -*-
#文本块生成器（util.py）
def lines(file):     #文件末尾追加空行
    for line in file:yield line
    yield '\n'

def blocks(file):
    block=[]
    for line in lines(file):
        if line.strip():    #非空行
            block.append(line)
        elif block:           #遇到空白行时（即文本块末尾），且block非空，则连接里面的行
            yield ' '.join(block).strip()
            bolck=[]