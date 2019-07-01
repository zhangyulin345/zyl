#简单的标记程序（simple_markup.py）
import  sys,re
from 简单的标记程序.utils import *

print ('<html><head><title>...</title><body>')

title=True
for block in blocks(sys.stdin):

    block=re.sub(r'\*(.+?)\*',r'<em>\1<em>',block)
    if title:
        print ('<h1>')
        print (block)
        print ('</h1>')
        title=False
    else:
        print ('<p>')
        print (block)
        print ('</p>')
        print ('</body></html>')