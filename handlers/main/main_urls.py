#coding=utf-8
from tornado.web import StaticFileHandler
# 静态文件处理器，与我们自定义的ProfileAddAvaterHandler类似
from main_handler import MainHandler
from handlers.account.account_urls import account_urls
from handlers.permission.permission_urls import permission_urls
from handlers.article.article_urls import article_urls
from handlers.files.files_urls import files_urls
from handlers.message.message_urls import message_urls

handlers = [
	(r'/',MainHandler),
	# 按照这个方式可以读取所有类似文件读取请求
	(r'/images/(.*\.(jpg|JPG|mp3|mp4|png))',StaticFileHandler,{'path':'files/'}),
]

handlers += account_urls # 导入handlers的urls

handlers += permission_urls # 导入权限管理模块的urls

handlers += article_urls # 导入文章管理模块

handlers += files_urls # 导入文件管理模块

handlers += message_urls # 导入消息模块