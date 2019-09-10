#coding=utf-8
from random import randint # 导入randint产生随机数
from datetime import datetime
from utils.captcha.captcha import create_captcha
from models.account.account_user_model import User
from libs.ytx_sms_python2.yun_tong_xun_lib import sendTemplateSMS # 导入短信验证信息



def create_captcha_img(self, pre_code, code):
	"""创建一个生成图形验证码并将其保存在redis数据库中的函数"""
	if pre_code:
		# 当pre_code存在时，就将其删除
		self.conn.delete("captcha:%s" % pre_code)
	# 调用创建图形参数，获取text,img;其中text不用获取，可以使用"_"占字符
	# 通过导入的utils文件中的create_captcha()函数生成图形验证码
	text, img = create_captcha()
	# 在redis数据库中设置code参数：键值对和过期时间，
	# self.conn.setex("captcha:%s" % code,text,60) # 图形验证码部分不分大小写
	self.conn.setex("captcha:%s" % code,text.lower(),60)  # 将图形验证码的英文部分都小写
	return img


def auth_captcha(self,captcha_code,code):
	"""定义一个图形验证码判别函数"""
	# captcha_code 是界面input框，自己输入的数据
	# if captcha_code: # 这种判断和if captcha_code == '
	# 比较而言的话，更加费时间，这里系统不知道captcha_code的数据类型
	# 就需要一个个数据类型比较是否为空。不如直接给出的''字符串效率高
	if captcha_code == '':
		return {'status':False,'msg':'请输入图形验证码！'}
	# 如果输入的图形验证码不等于界面的图形验证码时：
	elif self.conn.get('captcha:%s' % code) != captcha_code.lower():
		return {'status':False,'msg':'输入的图形验证码不正确！'}

	return {"status":True,'msg':'输入正确！'}



def login(self,name,password):
	"""定义一个登录函数"""
	if name == '' or password == '':
		return {'status':False,'msg':'请输入用户名和密码'}
	user = User.by_name(name)

	# 如果登录成功：
	if user and user.auth_password(password):
		user.last_login = datetime.now() # 上次登录时间
		user.loginnum += 1 # 登录次数+1
		self.db.add(user)
		self.db.commit() # 向数据库提交请求
		self.session.set('user_name',user.name) # 赋值一个user_name放在session中用来记录用户名，
		return {'status':True,'msg':'登录成功！'}
	return {'status':False,'msg':'用户名或密码错误！'}


def get_mobile_code_lib(self,mobile):
	"""产生手机验证码"""
	# 对手机号编码进行确认，如果为unicode编码，则转换为utf-8
	if isinstance(mobile,unicode):
		mobile = mobile.encode('utf-8')
	mobile_code = randint(1000,9999) # 获取随机数
	# 打印测试
	print '手机短信验证码是：',mobile_code
	self.conn.setex("mobile_code:%s"% mobile,mobile_code,2000) # 存入redis数据库

	# 短信验证码发送：
	# sendTemplateSMS(mobile,[mobile_code,30],1) # 手机号，验证码/30min有效，模板1

	return {'status': True, 'msg': '验证码发送到%s'%mobile}


def regist(self,mobile,mobile_captcha,code,name,password1,password2,captcha,agree):
	"""注册函数"""
	user = User.by_name(name)
	if user is not None:
		return {'status': False, 'msg': '用户名已经存在，请换一个名称'}

	if password1 != password2:
		return {'status': False, 'msg': '两次密码不一致'}

	if self.conn.get('mobile_code:%s'%mobile) != mobile_captcha:
		return {'status': False, 'msg': '短信验证码不正确'}

	if agree == "":
		return {'status':False,'msg':'您没有同意条款'}

	# 操作数据库内容
	user = User()
	user.name = name
	user.password =password2
	user.mobile = mobile
	self.db.add(user)
	self.db.commit() # 提交数据库
	return {'status':True}