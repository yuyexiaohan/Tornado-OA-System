#coding=utf-8

from handlers.base.base_handler import BaseHandler # 导入基本handler文件
from libs.account import account_auth_libs # 导入该文件，从该文件下导入定义的各个函数：导入创建图形验证码参数，登录验证码验证参数,导入登录函数



# 定义一个图形验证码函数
class CaptchaHandler(BaseHandler):
	"""01 生成验证码"""
	def get(self):
		# 获取参数
		pre_code = self.get_argument('pre_code','')
		code = self.get_argument('code','')

		print pre_code,code # 打印函数测试

		img = account_auth_libs.create_captcha_img(self,pre_code,code)  # 调用函数获取验证码
		# 设置响应头，将图片写入回去
		self.set_header("Content-type","image/jpg")
		self.write(img)


# 定义一个登录函数'
class LoginHandler(BaseHandler):
	"""02 登录函数"""
	def get(self):
		self.render('account/auth_login.html') # 返回注册界面


	def post(self):
		# 取参数
		name = self.get_argument('name','')
		password = self.get_argument('password','')
		code = self.get_argument('code','')
		captcha_code = self.get_argument('captcha','')

		# print name,password,code,captcha_code # 测试数据是否获取

		"""接受字符串判断的结果（False/True）"""
		result = account_auth_libs.auth_captcha(self,captcha_code,code)

		if result['status'] is False:
			# tornado中的write函数会对write函数的内容进行判断，
			# 如果时字典类型，就直接转换成字符串。我们自己就不用json方法转换了
			return self.write({'status':400, 'msg':result['msg']})

		# 得到login函数的返回字典，确定是登录成功或失败
		result = account_auth_libs.login(self,name,password)

		# 使用键"status"获取字典中对应的值：True/False
		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write({'status':400,'msg':result['msg']})


class RegistHandler(BaseHandler):
	"""03 注册函数"""
	def get(self):
		self.render('account/auth_regist.html',message='注册')
	# 	form表单请求，不是Ajax请求
	def post(self):
		mobile = self.get_argument('mobile','')
		mobile_captcha = self.get_argument('mobile_captcha','')
		code = self.get_argument('code','')
		name = self.get_argument('name','')
		password1 = self.get_argument('password1','')
		password2 = self.get_argument('password2','')
		captcha = self.get_argument('captcha','')
		agree = self.get_argument('agree','')

		"""接受字符串判断的结果（False/True）"""
		result = account_auth_libs.auth_captcha (self, captcha, code)

		if result['status'] is False:
			# tornado中的write函数会对write函数的内容进行判断，
			# 如果时字典类型，就直接转换成字符串。我们自己就不用json方法转换了
			return self.render ('account/auth_regist.html', message=result['msg'])

		# 用户注册
		result = account_auth_libs.regist(self,mobile,mobile_captcha,code,name,password1,password2,captcha,agree)
		if result['status'] is True:
			return self.redirect('/auth/user_login')
		return self.render('account/auth_regist.html',message = result['msg'])


class MobileCodeHandler(BaseHandler):
	"""04 获取手机验证码函数"""
	# ajax请求，返回网页代码，200，404，500等类型
	def post(self):
		mobile = self.get_argument('mobile','')
		code = self.get_argument('code','')
		captcha = self.get_argument('captcha','')

		print mobile,code,captcha # 打印验证数据是否获取成功

		"""获取图形验证码判断（False/True）"""
		result = account_auth_libs.auth_captcha (self, captcha, code)

		if result['status'] is False:
			# tornado中的write函数会对write函数的内容进行判断，
			# 如果时字典类型，就直接转换成字符串。我们自己就不用json方法转换了
			return self.write ({'status': 400, 'msg': result['msg']})
		"""获取手机号验证"""
		result = account_auth_libs.get_mobile_code_lib(self,mobile)

		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write({'status':200,'msg':result['msg']})


