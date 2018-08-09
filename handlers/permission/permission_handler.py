# coding=utf-8 
# @Time : 2018/8/5 22:16 
# @Author : achjiang
# @File : permission_handler.py 

from handlers.base.base_handler import BaseHandler
from libs.permission import permission_libs
from libs.permission.permission_auth.permission_interface_libs import handler_permission


class ManageHandler(BaseHandler):
	'''01管理者函数'''
	def get(self):
		roles, permissions, menus, handlers, users =  permission_libs.permission_manager_list_lib(self)
		kw = {
			'roles': roles,
			'permissions': permissions,
			'menus': menus,
			'handlers': handlers,
			'users': users,
			'dev_users': [],
		}

		return self.render('permission/permission_list.html',**kw)


class AddRoleHandler(BaseHandler):
	'''02添加角色'''
	def post(self):
		name = self.get_argument('name','')
		permission_libs.add_role_lib(self,name)
		self.redirect('/permission/manage_list')



class DelRoleHandler(BaseHandler):
	'''03删除角色'''

	@handler_permission('DelRoleHandler','handler')
	def get(self):
		roleid = self.get_argument('id','')
		permission_libs.del_role_lib(self,roleid)
		# 操作成功后，返回重定向到当前页面
		self.redirect ('/permission/manage_list')


class AddPermissionHandler(BaseHandler):
	'''04添加权限'''
	def post(self):
		name = self.get_argument('name','')
		strcode = self.get_argument('strcode','')

		permission_libs.add_permission_lib(self,name,strcode)
		# 操作成功后，返回重定向到当前页面
		self.redirect ('/permission/manage_list')


class DelPermissionHandler(BaseHandler):
	'''05删除权限'''
	def get(self):
		permissionid = self.get_argument('id','')
		permission_libs.del_permission_lib(self,permissionid)
		# 操作成功后，返回重定向到当前页面
		self.redirect ('/permission/manage_list')


class AddMenuHandler(BaseHandler):
	'''06添加菜单'''
	def post(self):
		name = self.get_argument('name','')
		permissionid = self.get_argument('permissionid','')
		permission_libs.add_menu_lib(self,name,permissionid)
		# 操作成功后，返回重定向到当前页面
		self.redirect ('/permission/manage_list')


class DelMenuHandler(BaseHandler):
	'''07删除菜单'''
	def get(self):
		menuid = self.get_argument('menuid','')
		permission_libs.del_menu_lib(self,menuid)
		# 操作成功后，返回重定向到当前页面
		self.redirect ('/permission/manage_list')



class AddHandlerHandler(BaseHandler):
	'''08添加处理器'''
	def post(self):
		name = self.get_argument('name','')
		permissionid = self.get_argument('permissionid','')
		permission_libs.add_handler_lib(self,name,permissionid)
		self.redirect('/permission/manage_list')



class DelHandlerHandler(BaseHandler):
	'''08删除处理器'''
	def get(self):
		handlerid = self.get_argument('handlerid','')
		permission_libs.del_handler_lib(self,handlerid)
		self.redirect('/permission/manage_list')



class AddUserRoleHandler(BaseHandler):
	'''09 给用户添加角色'''
	def post(self):
		roleid = self.get_argument('roleid','')
		userid = self.get_argument('userid','')
		permission_libs.add_user_role_lib(self,userid,roleid)
		self.redirect('/permission/manage_list')


class AddRolePermissionHandler(BaseHandler):
	'''10 给角色添加权限'''
	def post(self):

		roleid = self.get_argument('roleid','')
		permissionid = self.get_argument('permissionid','')
		permission_libs.add_role_permission_lib(self,roleid,permissionid)
		print 'test....'
		self.redirect('/permission/manage_list')


class DelUserRoleHandler(BaseHandler):
	'''11 删除用户角色'''
	def get(self):
		userid = self.get_argument('userid','')
		permission_libs.del_user_role_lib(self,userid)
		self.redirect('/permission/manage_list')


