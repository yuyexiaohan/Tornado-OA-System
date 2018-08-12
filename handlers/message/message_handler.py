# coding=utf-8 
# @Time : 2018/8/10 16:54 
# @Author : achjiang
# @File : message_handler.py
from datetime import datetime
import tornado.escape
from models.permission.permission_model import Role
from handlers.base.base_handler import BaseHandler,BaseWebSocketHandler

class SendMessageHandler(BaseWebSocketHandler):
	'''发送消息界面模块'''
	def get(self):
		kw = {
			'system_msg': self.get_readis_json_to_dict('system'),
			# 'system_msg': [],
			'role_msg': self.get_readis_json_to_dict('role'),
			# 'role_msg': [],
			'user_msg': self.get_readis_json_to_dict('user'),
			# 'user_msg': [],
			'roles': Role.all(),
		}

		self.render('message/message_send_message.html',**kw)

	def get_readis_json_to_dict(self,target):
		'''将readis存储的json字符串转换成可迭代的列表'''
		# lrange函数，是返回一个指定区间的列表
		msgs = self.conn.lrange('message:%s'%target, -5,-1)
		msgs.reverse() # 反转排序
		'''
		msgs:['{"content": "\\u603b\\u7ecf\\u7406\\u6d4b\\u8bd5", "send_type": "role", "datetime": "2018-08-10 22:19:11", "sender": "superuser", "target": "\\u603b\\u7ecf\\u7406"}', '{"content": "\\u4e2a\\u4eba\\u6d4b\\u8bd5\\u4fe1\\u606f", "send_type": "role", "datetime": "2018-08-10 22:18:39", "sender": "superuser", "target": "\\u603b\\u7ecf\\u7406"}']
				'''

		dict_list = []
		for m in msgs:
			# 解析遍历的字符串
			message_dict = tornado.escape.json_decode(m)
			dict_list.append(message_dict)
			'''
			dict_list:[{u'content': u'\u4e2a\u4eba\u6d4b\u8bd5\u4fe1\u606f', u'send_type': u'user', u'target': u'achjiang', u'sender': u'superuser', u'datetime': u'2018-08-10 22:18:05'}, {u'content': u'\u4e2a\u4eba\u6d4b\u8bd5\u4fe1\u606f', u'send_type': u'user', u'target': u'achjiang', u'sender': u'superuser', u'datetime': u'2018-08-10 22:17:42'}]
			'''
		return dict_list

	def post(self):
		content = self.get_argument('content','') # aaaaa 111
		user = self.get_argument('user','') # 222
		roleid = self.get_argument('roleid','')
		send_type = self.get_argument('send_type','')
		print content,user,roleid,send_type

		if send_type == "system":
			MessageWebHandler.send_system_message(self,content,send_type)
		if send_type == "role":
			MessageWebHandler.send_role_message(self, content, send_type, roleid)
		if send_type == "user":
			MessageWebHandler.send_user_message(self,content,send_type,user)
		self.redirect('/message/send_message')



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

	# ------------------提高部分 开始------------------
	@classmethod
	def send_system_message(cls, self, content, send_type):
		"""系统"""
		target = 'system'
		redis_msg = cls.dict_to_json (self, content, send_type, target)
		self.conn.rpush ('message:%s' % send_type, redis_msg)

		for f, v in MessageWebHandler.users.iteritems ():
			v.write_message (redis_msg)

	@classmethod
	def dict_to_json(cls, self, content, send_type, target):
		msg = {
			"content": content,
			"send_type": send_type,
			"sender": self.current_user.name,
			"target": target,
			"datetime": datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
		}
		return tornado.escape.json_encode (msg)

	@classmethod
	def send_role_message(cls, self, content, send_type, roleid):
		"""角色"""
		role = Role.by_id (roleid)
		redis_msg = cls.dict_to_json (self, content, send_type, role.name)
		self.conn.rpush ('message:%s' % send_type, redis_msg)
		role_users = role.users  # [zhangsan, lishi , wangwu]  [zhangsan, lishi]
		for user in role_users:
			if MessageWebHandler.users.get (user.name, None) is not None:
				MessageWebHandler.users[user.name].write_message (redis_msg)
			else:
				# self.conn.lpush("ws:role_off_line",message)
				pass

	@classmethod
	def send_user_message(cls, self, content, send_type, user):
		"""个人"""
		redis_msg = cls.dict_to_json (self, content, send_type, user)

		self.conn.rpush ('message:%s' % send_type, redis_msg)

		if cls.users.get (user, None) is not None:
			cls.users[user].write_message (redis_msg)
		else:
			# self.conn.lpush("ws:user_off_line",message)
			pass

	# ------------------提高部分 结束------------------


	# ------------------掌握的部分 开始------------------
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

		# 将变量进行json编码，得到一个json类型的字符串
		message = tornado.escape.json_encode (msg)
		# redis数据库的rpush方法是指将一个数据存放在一个列表的最右边，
		# 如果列表不存在，则创建这个列表并将数据存放在最右端
		# 这里将创建一个
		self.conn.rpush('message:list001',message)

		# 1.如果列表中定义了一个用户，只能单向的给这个用户发信息
		# MessageWebHandler.users['achjiang'].write_message (message)  # self是当前的实例

		# 2.如果给多个用户发的话，可以使用for循环遍历下
		# iteritems是将字典内的数据遍历出来，键存放在f,值存放在v
		for f,v in MessageWebHandler.users.iteritems():
			v.write_message(message)

		# self.conn.rpush ('message:list001', message)

# ------------------掌握的部分 结束------------------