# coding=utf-8
# @Time : 2018/8/5 13:57 
# @Author : achjiang
# @Site :  
# @File : account_libs.py 
# @Software: PyCharm
from string import printable
from random import choice
from datetime import datetime
from uuid import uuid4 # 导入为4的随机数模块
import json
from libs.common.send_email.send_email_libs import send_qq_html_email # 导入网页发送信息
import traceback


def edit_profile(self,name,password):
	'''编辑个人信息'''
	if password == '':
		return {'status':False,'msg':'密码不能为空！'}

	if name == '':
		return {'status':False,'msg':'姓名不能为空！'}
	# current_user 已经缓存一次，可以直接调用
	user = self.current_user
	user.name = name
	user.password = password
	user.update_time = datetime.now()
	self.db.add(user)
	self.db.commit()
	self.session.set('user_name',user.name)
	return {'status':True,'msg':'修改成功！'}



def send_email_libs(self,email):
	'''发送邮箱绑定信息'''
	if email == '':
		return {'status':False,'msg':'邮箱不能为空！'}

	# 邮箱验证码，创建的随机的4个字符串
	email_code = ''.join([choice(printable[:62]) for i in xrange(4)])

	# 4个代表用户的字符串
	u = str(uuid4)

	# 将邮箱验证字符串和用户随机验证的4个字符串以键值对的形式放入字典中
	text_dict = {
		u:self.current_user.id,
		'email_code':email_code
	}

	# 使用json将字典序列化成字符串
	redis_dict = json.dumps(text_dict)
	# 将数据（邮箱地址/用户随机4为字符串/当前对应用户id/邮箱随机4为验证码）保存到redis中，并设置过期时间为500
	self.conn.setex('email:%s' % email,redis_dict,500)
	# 创建一个要发送给邮箱的内容content
	# 链接中携带三个参数，分别是code,email,user_id
	content = """
		<p>html 邮件</p>
		<p><a href="http://127.0.0.1:8000/account/auth_email_code?code={}&email={}&user_id={}">点击绑定邮箱</a></p>
	""".format(email_code,email,u)  # format与%s类似，将模板内的空值赋值

	# 调用发送邮箱请求函数，将发件人邮箱信息及收件人邮件信息，邮箱标题，邮箱内容发送
	send_qq_html_email("369668247@qq.com",[email],"tornado测试",content)
	# 发送完成，返回发送成功信息
	return {'status':True,'msg':'邮箱发送成功'}


def auth_email_libs(self,email_code,email,u):
	'''个人邮件信息确认'''
	# 从redis数据库中获取该邮箱数据
	redis_text = self.conn.get('email:%s'% email)
	# 如果获取到邮箱
	if redis_text:
		text_dict = json.loads(redis_text) # 将获得数据序列化

		# 对比数据库存的邮箱随机验证字符串和实际的是否一致
		if text_dict and text_dict['email_code'] == email_code:
			user = self.current_user # 一致就获取当前用户
			if not user:
				user = user.by_id(text_dict[u]) # 如果没有用户则，从数据库中的u匹配对应的用户id,获取该用户
			# 将该用户的个人邮箱设置为函数返回的邮箱
			user.email = email
			# 数据更新时间为当前时间
			user.update_time =datetime.now()
			# 数据添加到mysql数据库中
			self.db.add(user)
			# 向数据库发送请求
			self.db.commit()
			# 返回绑定成功信息
			return {'status':True,'msg':'邮箱修改成功！'}
		# 否则，返回邮箱不正确信息
		return {'status':False,'msg':'邮箱验证不正确！'}
	# 因为发送的邮箱信息设置有过期时间，当时间到后，redis数据库中就会删除该信息，则无法匹配存储的邮箱等相关信息
	return {'status': False, 'msg': '邮箱验证码已过期，请重新绑定！'}



def add_avatar_lib(self,body):
	'''添加图像'''
	try:
		user = self.current_user # 获取当前用户

		# 将去除的body作为user的图像进行存储
		# 给avatar赋值一般是user.avatar(body),这里这样通过等号的方式进行赋值书写更加方便，但具体由那个方式去赋值，是由.avatar方法定义
		user.avatar = body
		user.update_time = datetime.now()
		self.db.add(user)
		self.db.commit()
		return {'status':True}
	except Exception as e:
		print '-'*20
		print traceback.format_exc() # 将错误异常打印在服务器上
		print '-'*20
	return {'status':False,'msg':'error'}

