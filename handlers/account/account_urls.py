#coding=utf-8

#方式一： from account_auth_handler import LoginHandler
#方式二：
import account_auth_handler
import account_handler

account_urls = [
	# 用户注册相关url
	(r'/auth/user_login',account_auth_handler.LoginHandler),
	(r'/auth/captcha',account_auth_handler.CaptchaHandler),
	(r'/auth/user_regist',account_auth_handler.RegistHandler),
	(r'/auth/mobile_code',account_auth_handler.MobileCodeHandler),

	# 账户注册url
	(r'/account/user_profile',account_handler.ProfileHandler),
	(r'/account/user_edit',account_handler.ProfileEditHandler),
	(r'/account/send_user_email',account_handler.ProfileModifyEmailHandler),
	(r'/account/auth_email_code',account_handler.ProfileAuthEmailHandler),
	(r'/account/avatar',account_handler.ProfileAddAvaterHandler),

	# 文档相关url


]