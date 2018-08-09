# coding=utf-8 
# @Time : 2018/8/6 15:20 
# @Author : achjiang
# @File : permission_interface_libs.py
from models.permission.permission_model import Menu,Handler

# 定义一个字典，将处理器模型及菜单模型以字典的形式放入
obj_model = {
    "handler": Handler,
    "menu": Menu,

}
class PermissionAuth(object):
    # 用户权限管理
    def __init__(self):
        self.user_permission = set() #当前用户的所有权限
        self.obj_permission = ''

    def permission_auth(self, user,  name, types, model):
        #获取当前用户的权限
        print '=====permission_auth====='
        roles = user.roles
        # 通过for循环遍历，得到当前用户权限码，放入集合
        for role in roles:
            for permission in role.permissions:
                self.user_permission.add(permission.strcode)

        #获取handler、menu的权限
        # obj_model['handler'] == Handler.by_name('')
        # obj_model['menu']  == Menu .by_name('')

        # 根据1.用户传入的数据类型（types）的方式查找，obj_model字典
        # 查找到对应的数据类型，如果是Menu，就是菜单，如果是
        # Handler就是处理器2.用户名查询
        handler = model[types].by_name(name) # 这里的handler只是一个变量，随[types]键查找到对应的数据类型
        # 如果查询不到，则直接返回False表示没有模板权限
        if handler is None:
            return False
        permission = handler.permission # 获取查询的handler权限
        self.obj_permission = permission.strcode #获取该权限的权限码

        #如果handler对应的权限存在用户的所有权限集合中，返回True
        print '-'*50
        print self.user_permission
        print self.obj_permission
        print '-' * 50
        if self.obj_permission in self.user_permission: # if  'files_manage_menu' in {'files_manage_menu'}
            return True
        return False

def menu_permission(self, menuname, types):
    '''根据返回值，真显示该函数包裹的html界面，否则，不显示'''
    # 将当前用户，菜单名，类型等传入进行判断
    if PermissionAuth().permission_auth(self.current_user, menuname, types, obj_model):
        return True
    return False


def handler_permission(handlername, types):
    # 处理器权限管理装饰器
    def func(method):
        def wrapper(self, *args, **kwargs):
            if PermissionAuth().permission_auth(self.current_user, handlername, types, obj_model):
                return method(self, *args, **kwargs)
            else:
                self.write('您没有权限')
        return wrapper
    return func




'''
def menu_permission(self,menuname,types):
	# 菜单权限管理
	menu = Menu.by_name(menuname) # 通过菜单名获取菜单
	menu_p = menu.permission # 菜单关联管理权限表
	print menu_p.strcode # 获得权限码

	# 获取当前表的所有角色
	user_roles = self.current_user.roles # 这里得到的roles是一个列表
	# 逐步获取单个role,并逐步获取role中的permission
	for role in user_roles:
		for permission in role.permissions:
			print permission.name,permission.strcode
			# 使用模板获取用户的权限码与当前用户的权限码作比较，
			# 相等的时候说明当前用户有模板上的权限，这样就让'菜单管
			# 理权限函数返回True,这样前端就能显示该模板，否则返回
			# False，前端不显示该部分权限
			if menu_p.strcode == permission.strcode:
				return True
			else:
				return False
'''

