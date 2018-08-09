#coding=utf-8

from handlers.base.base_handler import BaseHandler # 导入基本handler文件
from libs.account import account_libs


class ProfileHandler(BaseHandler):
	'''个人主界面'''
	def get(self):
		self.render('account/account_profile.html',message=None)


class ProfileEditHandler(BaseHandler):
	'''个人信息编辑'''
	def get(self):
		self.render('account/account_edit.html')

	def post(self):
		name = self.get_argument('name','')
		password = self.get_argument('password','')
		print name,password

		result = account_libs.edit_profile(self,name,password)

		if result['status'] is False:
			return self.render('account/account_profile.html',message=result['msg'])
		return self.render('account/account_profile.html',message=result['msg'])


class ProfileModifyEmailHandler(BaseHandler):
	'''个人邮箱，绑定提交'''
	def get(self):
		self.render('account/account_send_email.html')

	def post(self):
		email = self.get_argument('email','')
		print email

		result = account_libs.send_email_libs(self,email)

		if result['status'] is True:
			return self.write(result['msg'])


class ProfileAuthEmailHandler(BaseHandler):
	'''个人绑定邮箱验证'''
	def get(self):
		email_code = self.get_argument('code','')
		email = self.get_argument('email','')
		u = self.get_argument('user_id','')

		result = account_libs.auth_email_libs(self,email_code,email,u)
		if result['status'] is True:
			return self.redirect('/account/user_edit')
		return self.write(result['msg'])


class ProfileAddAvaterHandler(BaseHandler):
	'''文件上传'''
	def post(self):
		avatar_data = self.request.files.get('user_avatar','')
		print avatar_data
		'''
		使用一个只有123abc的txt文件，测试打印输出为:
		[{'body': '123abc', 'content_type': u'text/plain', 'filename': u'tornado\u4e0a\u4f20\u6587\u4ef6\u6d4b\u8bd5.txt'}]
		其中：
		'body':上传的文件内容，如果是文件的话，就是一个二进制的代码；
		'content_type'：数据类型；
		'filename':文件名，汉字以二进制的方式进行测试；
		'''
		# 由上面举例可以知道，通过avatar_data[0]['body']的方式可以取到内容，即为上传文件的内容，通过add_avatar_lib()方法存储到mysql数据库
		result = account_libs.add_avatar_lib(self,avatar_data[0]['body'])
		if result['status'] is True:
			return self.redirect('/account/user_edit')
		return self.write(result['msg'])
