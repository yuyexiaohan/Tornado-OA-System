# coding=utf-8 
# @Time : 2018/8/5 22:16 
# @Author : achjiang
# @Site :  
# @File : permission_urls.py
# @Software: PyCharm
import permission_handler

permission_urls = [
	(r'/permission/manage_list',permission_handler.ManageHandler),
	(r'/permission/add_role',permission_handler.AddRoleHandler),
	(r'/permission/del_role',permission_handler.DelRoleHandler),
	(r'/permission/add_permission',permission_handler.AddPermissionHandler),
	(r'/permission/del_permission',permission_handler.DelPermissionHandler),
	(r'/permission/add_menu',permission_handler.AddMenuHandler),
	(r'/permission/del_menu',permission_handler.DelMenuHandler),
	(r'/permission/add_handler', permission_handler.AddHandlerHandler),
	(r'/permission/del_handler', permission_handler.DelHandlerHandler),
	(r'/permission/user_add_role', permission_handler.AddUserRoleHandler),
	(r'/permission/role_add_permission', permission_handler.AddRolePermissionHandler),
	(r'/permission/del_user_role', permission_handler.DelUserRoleHandler),

]