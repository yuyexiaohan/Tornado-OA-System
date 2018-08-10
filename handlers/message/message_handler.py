# coding=utf-8 
# @Time : 2018/8/10 16:54 
# @Author : achjiang
# @File : message_handler.py
from datetime import datetime
import tornado.escape
from models.permission.permission_model import Role
from handlers.base.base_handler import BaseHandler,BaseWebSocketHandler

class MessageHandler(BaseHandler):
	'''消息模块'''
	def get(self):
		kw = {'cache':''}
		self.render('message/message_chat.html',**kw)


class MessageWebHandler(BaseWebSocketHandler):
	'''网页消息模块'''
	# 创建一个用户字典，用开区分是哪些用户
	# {'用户名':MessageWebHandler.users}
	users = {}
	'''当同时2个用户使用时光说说时：MessageWebHandler.users=
	{u'superuser': <handlers.message.message_handler.MessageWebHandler object at 0xb5f965ec>, 
	u'achjiang': <handlers.message.message_handler.MessageWebHandler object at 0xb5f4be2c>}
	'''
	def open(self):
		# 这个类定义的参数，可以使用类名去调用,得到一个self
		MessageWebHandler.users[self.current_user.name] = self
		print MessageWebHandler.users
		pass
	def on_close(self):
		pass
	def on_message(self,message):
		'''发送信息'''
		# {"content_html":"123"}
		print message

		msg = tornado.escape.json_decode(message) # 转码为字符串
		msg.update({
			'name':self.current_user.name,
			'useravatar':self.current_user.avatar,
			'datetime':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		})

		message = tornado.escape.json_encode (msg)
		# 1.如果列表中定义了一个用户，只能单向的给这个用户发信息
		# MessageWebHandler.users['achjiang'].write_message (message)  # self是当前的实例

		# 2.如果给多个用户发的话，可以使用for循环遍历下
		# iteritems是将字典内的数据遍历出来，键存放在f,值存放在v
		for f,v in MessageWebHandler.users.iteritems():
			v.write_message(message)


		# self.conn.rpush ('message:list001', message)