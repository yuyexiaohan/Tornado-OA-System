# coding=utf-8 
# @Time : 2018/8/5 23:12 
# @Author : achjiang
# @File : permission_libs.py
from models.permission.permission_model import Role,Permission,Menu,Handler # 引入的是实体表
from models.account.account_user_model import User
from libs.flash.flash_lib import flash # 导入消息提示方法


def permission_manager_list_lib(self):
	# 获取所有的角色/权限/菜单/处理器/用户
	roles = Role.all()
	permissions= Permission.all()
	menus = Menu.all()
	handlers = Handler.all()
	users = User.all()

	return roles,permissions,menus,handlers,users


def add_role_lib(self,name):
	'''02添加一个角色'''
	if not name:
		flash (self, '请输入角色名称！', 'error')
		return
	print type(name),'name:%s'%name
	role = Role.by_name(name)
	if role is not None:
		flash(self,'角色已经存在！','error')
		return
	role = Role()
	role.name = name
	self.db.add(role)
	self.db.commit()
	flash(self,'角色添加成功！','success')

def del_role_lib(self,roleid):
	'''03删除角色'''
	role = Role.by_id(roleid) # 获取用户信息
	# 判断角色是否存在
	if role is None:
		flash (self, '角色删除失败！', 'error')
		return
	self.db.delete(role)
	self.db.commit()
	flash (self, '角色删除成功！', 'success')


def add_permission_lib(self,name,strcode):
	'''04添加权限'''
	if not name or not strcode:
		flash(self,'请输入权限名和权限码！','error')
		return
	permission = Permission.by_name(name)
	# 如果权限有，就不用添加
	if permission is not None:
		flash (self, '权限已存在！', 'error')
		return
	permission = Permission()
	permission.name = name
	permission.strcode = strcode
	self.db.add(permission)
	self.db.commit()
	flash (self, '权限添加成功！', 'success')



def del_permission_lib(self,permissionid):
	'''05删除权限'''
	permission = Permission.by_id(permissionid)
	# 判断该权限id获取值是否为空
	if permission is None:
		flash (self, '权限不存在，删除失败！', 'error')
		return
	self.db.delete(permission)
	self.db.commit()
	flash (self, '权限删除成功！', 'success')


def add_menu_lib(self,name,permissionid):
	'''06添加菜单'''
	if not name or not permissionid:
		flash(self,'请输入菜单名和权限码！','error')
		return
	permission = Permission.by_id(permissionid)
	# 判断权限是否存在，不存在直接返回，存在，在验证菜单部分
	if permission is None:
		flash (self, '该权限id不存在！', 'error')
		return
	menu = Menu.by_name(name)
	# 如果菜单是空，则创建
	if menu is None:
		menu = Menu()
	menu.name = name
	# 问题，这里可不可以添加进去
	# 方法1：通过orm的方式添加数据
	# menu.permission = permission
	# 方法2：同过数据库字段的方式添加数据
	menu.p_id = permissionid
	print menu.p_id
	self.db.add(menu)
	self.db.commit()
	flash (self, '菜单添加成功！', 'success')


def del_menu_lib(self,menuid):
	'''07删除菜单'''
	menu = Menu.by_id(menuid)
	# 判断该菜单id获取值是否为空
	if menu is None:
		flash (self, '菜单不存在，删除失败！', 'error')
		return
	self.db.delete(menu)
	self.db.commit()
	flash (self, '菜单删除成功！', 'success')


def add_handler_lib(self,name,permissionid):
	'''08添加处理器'''
	if not name or not permissionid:
		flash(self,'请输入处理器或权限id！', 'error')
	permission = Permission.by_id(permissionid)
	# 判断权限是否存在，不存在直接返回，存在，在验证菜单部分
	if permission is None:
		flash (self, '该权限id不存在！', 'error')
		return
	handler = Handler.by_name(name)
	# 如果权限是空，则创建
	if handler is None:
		handler = Handler()
	handler.name = name
	# 问题，这里可不可以添加进去
	# 方法1：通过orm的方式添加数据
	# handler.permission = permission
	# 方法2：同过数据库字段的方式添加数据
	handler.p_id = permissionid
	self.db.add(handler)
	self.db.commit()
	flash (self, '处理器添加成功！', 'success')


def del_handler_lib(self,handlerid):
	'''09删除处理器'''
	handler = Handler.by_id(handlerid)
	# 判断该c处理器id获取值是否为空
	if handler is None:
		flash (self, '处理器不存在，删除失败！', 'error')
		return
	self.db.delete(handler)
	self.db.commit()
	flash (self, '处理器删除成功！', 'success')


def add_user_role_lib(self,userid,roleid):
	'''10 给用户添加角色'''
	if not userid or not roleid:
		flash(self,'请输入用户id和角色id!','error')
		return
	user = User.by_id(userid)
	role = Role.by_id(roleid)
	if user is None or role is None:
		flash (self, '用户id或角色id不存在！', 'error')
		return
	user.roles.append(role) # 多对多关系添加
	# role.users.append(user)

	self.db.add(user)
	self.db.commit()
	flash (self, '给用户添加角色成功！', 'success')



def add_role_permission_lib(self,roleid,permissionid):
	'''11 给角色添加权限'''
	if not permissionid or not roleid:
		flash(self,'请输入角色id!和权限id!','error')
		return
	permission = Permission.by_id(permissionid)
	role = Role.by_id(roleid)

	if permission is None or role is None:
		flash (self, '角色id或权限id不存在！', 'error')
		return
	permission.roles.append (role)  # 多对多关系添加,数组添加
	print 'permission%s'%permission
	self.db.add (permission)
	self.db.commit ()
	flash (self, '给角色添加权限成功！', 'success')


def del_user_role_lib(self,userid):
	'''12 删除用户角色'''
	user = User.by_id(userid)
	if user is None:
		flash (self, '用户角色不存在，删除失败！', 'error')
		return
	self.db.delete(user)
	self.db.commit()
	flash (self, '用户删除成功！', 'success')




