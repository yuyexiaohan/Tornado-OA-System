# coding=utf-8 
# @Time : 2018/8/8 11:01 
# @Author : achjiang
# @File : files_libs.py
from uuid import  uuid4
from datetime import datetime
from models.files.upload_file_model import Files
# ---------分享部分---------
from random import choice
from string import printable
import json
# ---------分享部分---------
# 七牛云文件上传模块
from libs.qiniu.qiniu_libs import upload_qiniu_file_content,down_qiniu_file

from tornado.concurrent import run_on_executor

def files_list_lib(self):
	'''文件列表'''
	files = Files.all()
	return files


def upload_files_lib(self,upload_files):
	'''文件上传'''
	img_path_list = []
	for upload_file in upload_files:
		file_path = save_file(self,upload_file)
		print 'file_path:%s'%file_path
		img_path_list.append(file_path)
	return img_path_list if img_path_list else None
# 	最后return的是一个带有相关信息的数组
'''
[
    {'status': False, 'msg': '文件格式不正确', 'data':''},
    {'status': True, 'msg': '文件保存成功(其实以前有人上传过了)', 'data':file_path}
    {'status': True, 'msg': '文件保存成功', 'data': file_path}
]
'''



def save_file(self,upload_file):
	'''保存文件'''
	# [{'body': '123abc', 'content_type': u'text/plain', 'filename': u'tornado\u4e0a\u4f20\u6587\u4ef6\u6d4b\u8bd5.txt'}]
	# 获取文件扩展名(.jpg)
	# 使用split方法以'.'为切割对象，得到一个列表，然后取列表的最后一个元素既是文件扩展名
	files_ext = upload_file['filename'].split('.')[-1]
	# 判断上传文件的格式，不是的返回格式不正确，是，执行上传数据库
	if files_ext not in ['jpg','JPG','bmp','png','ogg','mp3','mp4']:
		return {'status': False, 'msg': '文件格式不正确', 'data': ''}
	# 定义一个文件名字
	# uuidname = cf43df90-0602-4416-a2b0-9fd814c0e2f2.jpg
	# uuid4() 随机生成16个一组的随机数，每个随机数使用2位十六进制表示，
	'''
	        if version is not None:
            if not 1 <= version <= 5:
                raise ValueError('illegal version number')
            # Set the variant to RFC 4122.
            # int = int & ~(0xc000 << 48L)
            int &= ~(0xc000 << 48L)
            int |= 0x8000 << 48L
            # Set the version number.
            int &= ~(0xf000 << 64L)
            int |= version << 76L
        self.__dict__['int'] = int
	'''


	uuidname = str (uuid4 ()) + '.%s' % files_ext

	file_content = upload_file['body']
	# 判断文件是否存在
	old_file = Files.file_is_existed (file_content)
	if old_file is not None:
		file_path = 'http://192.168.10.128:9000/images/' + old_file.uuid  # url
		return {'status': True, 'msg': '文件保存成功(以前有人上传过啦)', 'data': file_path}

	# 如果文件不存在：保存文件（路径）
	## 保存文件
	path = 'files/' + uuidname  # 文件保存的硬盘路径
	# 打开文件，wb是二进制保存文件
	with open (path, 'wb') as f:
		f.write (file_content)

	files = Files () # 实例化一个对象
	files.filename = upload_file['filename'] # 取出文件名
	files.uuid = uuidname
	files.content_length = len (file_content) # 计算文件长度
	files.content_type = upload_file['content_type'] # 文件类型
	files.update_time = datetime.now () # 上传时间
	files.file_hash = file_content # 上传的文件hash值，用于文件是否存在的判断

	files.files_users.append (self.current_user) # 上传文件用户
	self.db.add (files) # 添加到数据库
	self.db.commit ()
	# http://127.0.0.1:8000/images/cf43df90-0602-4416-a2b0-9fd814c0e2f2.jpg
	# http://127.0.0.1:8000/images/83a3b62b-384a-4fce-8c7e-47ac1910b331.jpg
	file_path = 'http://127.0.0.1:8000/images/' + uuidname
	return {'status': True, 'msg': '文件保存成功', 'data': file_path}



'''代码原则：常量都要定义到配置文件当中

[
    {'status': False, 'msg': '文件格式不正确', 'data':''},
    {'status': True, 'msg': '文件保存成功(其实以前有人上传过了)', 'data':file_path}
    {'status': True, 'msg': '文件保存成功', 'data': file_path}
]
'''


def files_message_lib(self,uuid):
	'''获取文件详情'''
	files = Files.by_uuid(uuid)
	return files


def files_pag_list_lib(self,page):
	'''文件列表'''
	files = self.current_user.users_files # 获取当前用户当前文件
	files_pag = get_page_list(int(page),files,2) # 当前页数
	files_del = self.current_user.users_files_del # 删除页数
	return files_pag['files'],files_pag,files_del

def get_page_list(current_page,content,MAX_PAGE):
	'''获取当前页码 MAX_PAGE:一页展示的文件数'''
	# 当前页起始文章：当前页减一，得到列表的索引值
	start = (current_page - 1) * MAX_PAGE
	# 当前页结束文章：当页开始文章加最多显示文章，为当前页显示文章
	end = start + MAX_PAGE
	split_content = content[start:end]

	total = content.count() # 统计总共的文章数
	count = total/MAX_PAGE

	if total % MAX_PAGE !=0:
		count += 1
	pre_page = current_page - 1 # 上一页
	next_page = current_page + 1 # 下一页
	if pre_page == 0:
		pre_page = 1
	if next_page > count:
		next_page = count

	# range：是生成一个列表，xrange是生成一个数字
	if count < 5:
		pages = [ p for p in xrange(1,count-1) ] # [1,2,3,4]
	elif current_page <= 3:
		pages = [ p for p in xrange(1,6) ] #[1,2,3,4,5]

	elif current_page >= count-2:
		pages = [ p for p in xrange(count-4,count+1) ] # 1,2...[8,9,10]
	else:
		pages = [ p for p in xrange(current_page-2,current_page+3) ]
	return {
		'files':split_content,
		'count':count,
		'pre_page':pre_page,
		'next_page':next_page,
		'current_page':current_page,
		'pages':pages,
	}


def files_delete_lib(self,uuid):
	'''删除文件'''
	files = Files.by_uuid(uuid)
	# 删除文件关联表关系
	files.files_users.remove(self.current_user)
	# 将当前文件放入删除文件表中
	files.files_users_del.append(self.current_user)
	self.db.add(files)
	self.db.commit()


def files_recovery_lib(self,uuid):
	'''文件恢复'''
	files = Files.by_uuid(uuid)
	files.files_users.append(self.current_user)
	files.files_users_del.remove(self.current_user)
	self.db.add(files)
	self.db.commit()

# 实际只是删除了关联表，并未真的删除文件表
def files_delete_final_lib(self,uuid):
	'''彻底删除文件'''
	files = Files.by_uuid(uuid)
	files.files_users_del.remove(self.current_user)
	# self.current_user.users_files_del.remove(files) # 等效于上面的删除句子
	self.db.add(files)
	self.db.commit()


#-----------------------------分享链接处理器--(可以用另一个用户登录后分享文件)-----------------------------
def create_sharing_links_lib(self, file_uuid):
    """001创建分享链接"""
    #生成redis键
    uu = str(uuid4())
    #生成4位提取密码
    password = ''.join([choice(printable[:62]) for i in xrange(4)])
    #创建字典
    redis_dict = {
        'user': self.current_user.name,
        'file_uuid': file_uuid,
        'password': password
    }
    #序列化字典
    reids_json = json.dumps(redis_dict)
    #保存到redis中
    self.conn.setex('sharing_links:%s' % uu, reids_json, 300)
    return 'http:127.0.0.1:8000/files/files_auth_sharing_links?uuid=%s'%uu, password


def get_username_lib(self,uu):
    """001获取分享者姓名"""
    #查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    #如果没有返回过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    #如果有反序列化，返回用户名
    redis_dict = json.loads(redis_json)
    return {'status':True, 'msg':'', 'username': redis_dict['user']}



def get_sharing_files_lib(self, uu, password):
    """002使用密码验证分享链接"""
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    #对比用户提交的密码与redis保存的密码
    if password == redis_dict['password']:
        #对比成功，密码保存当前用户的session
        self.session.set('sharing_links_password', password)
        #返回分享链接
        links = '/files/files_sharing_list?uuid=%s' % uu
        return {'status': True, 'msg': '分享11111成功', 'links': links, 'username':''}
    return {'status':False, 'msg': '分享密码输入错误', 'username': redis_dict['user']}


def files_sharing_list_lib(self, uu):
    """003查看分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    #获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        #如果没有密码重新获取链接
        return {'status': False, 'msg': '请重新获取链接', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 返回文件
    files = Files.by_uuid(redis_dict['file_uuid'])
    return {'status': True, 'msg': '分享成功', 'data': [files], 'uuid':uu}


def save_sharing_files_lib(self, uu):
    """004保存分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    # 获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        # 如果没有密码重新获取链接
        return {'status': False, 'msg': '没有权限', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 把文件保存到当前用户


    files = Files.by_uuid(redis_dict['file_uuid'])
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    return {'status': True, 'msg': '保存成功', 'data': ''}


#-----------------------------分享链接处理器结束-------------------------------

#-----------------------------七牛云上传下载文件开始-------------------------------
def upload_files_qiniu_lib(self, upload_files):
    """03文件上传到七牛服务器"""
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_qiniu_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def save_qiniu_file(self, upload_file):
    """03保存单个文件到七牛"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}

    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://oq54v29ct.bkt.clouddn.com/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(其实文件在硬盘上)', 'data': file_path}

    #上传到七牛
    # with open(path, 'wb') as f:
    #     f.write(file_content)

    ret, info = upload_qiniu_file_content(file_content)
    print ret
    print info
    if info.status_code != 200:
        return {'status': False, 'msg': '文件上传到七牛失败', 'data': ''}

    file_name = upload_file['filename']
    files = Files()
    files.filename = file_name
    files.uuid = ret #保存的七牛返回的文件名
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.update_time = datetime.now()
    files.file_hash = upload_file['body']
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://oq54v29ct.bkt.clouddn.com/' + files.uuid
    return {'status': True, 'msg': '文件上传到七牛成功', 'data': file_path}


def files_download_qiniu_lib(self, uuid):
    """04从七牛服务器下载文件"""
    if uuid == '':
        return {'status':False, 'msg': '没有文件ID'}
    old_file = Files.by_uuid(uuid)
    if old_file is None:
        return {'status': False, 'msg': '文件不存在'}
    qiniu_url = 'http://oq54v29ct.bkt.clouddn.com/%s' % uuid
    url = down_qiniu_file(qiniu_url)
    print url
    return {'status': True, 'data': url}

#-----------------------------七牛云上传下载文件结束-------------------------------


#重点掌握
@run_on_executor
def files_download_lib(self, uuid):
    filepath = 'files/%s' % uuid
    self.set_header("Content-Type", "application/octet-stream")
    self.set_header("Content-Disposition", 'attachment; filename=%s' % uuid)
    with open(filepath, 'rb') as f:
        while 1:
            data = f.read(1024*5)
            print len(data)
            if not data:
                break
            self.write(data)
            self.flush()
            #time.sleep(0.2) # 加时间延迟，下载会按照这个时间下载完成

    self.finish() # 完成后，结束进程


