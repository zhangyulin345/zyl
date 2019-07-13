# 导入服务器模块
from http.server import HTTPServer, CGIHTTPRequestHandler
# 端口
PORT = 8000
# 创建服务器对象
httpd = HTTPServer(("", PORT), CGIHTTPRequestHandler)
print("serving at port", PORT)
# 反复处理连接请求
httpd.serve_forever()
