# coding=utf-8 
# @Time : 2018/8/8 8:59 
# @Author : achjiang
# @File : files_handler.py
from handlers.base.base_handler import BaseHandler
from libs.files import files_libs

class FilesListHandler(BaseHandler):
	'''文件列表'''
	def get(self):
		files = files_libs.files_list_lib(self)
		kw = {'files':files}
		return self.render('files/files_list.html', **kw )


class FilesUploadHandler(BaseHandler):
	'''上传文件'''
	def get(self):
		return self.render('files/files_upload.html')

	def post(self):
		'''ajax请求'''
		# 获取文件，'imporfile'时前端的文件名
		upload_files = self.request.files.get('importfile','')
		# print 'upload_files:%s' % upload_files
		result = files_libs.upload_files_lib(self,upload_files)
		print 'result:%s'%result
		if result is None:
			return self.write({'status':400,'msg':'文件上传出错！'})
		return self.write({'status':200,'msg':'保存成功！','data': result})



class FilesMessageHandler(BaseHandler):
	'''文件详情'''
	def get(self):
		uuid = self.get_argument('uuid','')
		files = files_libs.files_message_lib(self,uuid)
		kw = {'files':files}
		return self.render('files/files_message.html',**kw)


class FilesPagListHandler(BaseHandler):
	'''文章列表'''
	def get(self,page):
		files,files_page,files_del = files_libs.files_pag_list_lib(self,page)
		kw = {
			'files': files,
			'files_page': files_page,
			'files_del': files_del,
		}
		return self.render('files/files_page_list.html',**kw)


class FilesDeleteHandler(BaseHandler):
	'''删除文件'''
	def get(self):
		uuid = self.get_argument('uuid','')
		files_libs.files_delete_lib(self,uuid)
		return self.redirect('/files/files_page_list/1')


class FilesRecoveryHandler(BaseHandler):
	'''回复删除文件'''
	def get(self):
		uuid = self.get_argument('uuid','')
		files_libs.files_recovery_lib(self,uuid)
		return self.redirect('/files/files_page_list/1')


class FilesDeletFinalHandler(BaseHandler):
	'''彻底删除文件'''
	def get(self):
		uuid = self.get_argument('uuid','')
		files_libs.files_delete_final_lib(self,uuid)
		return self.redirect('/files/files_page_list/1')


#-----------------------------分享链接处理器-------------------------------
class FilesCreateSharingLinks(BaseHandler):
    """001创建分享链接"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        fileslinks, password = files_libs.create_sharing_links_lib(self, uuid)
        kw = {'fileslinks': fileslinks, 'password': password}
        self.render('files/files_create_sharing_links.html', **kw)


class FilesAuthSharingLinks(BaseHandler):
    """002使用密码验证分享链接"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = files_libs.get_username_lib(self, uu)
        if result['status'] is False:
            kw = {'username': result['username'], 'uuid1': uu, 'msg': result['msg']}
            return self.render('files/files_auth_sharing_links.html', **kw)
        kw = {'username': result['username'], 'uuid1': uu, 'msg': ''}
        self.render('files/files_auth_sharing_links.html', **kw)

    def post(self):
        uu = self.get_argument('uuid', '')
        password = self.get_argument('password', '')
        result = files_libs.get_sharing_files_lib(self, uu, password)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        return self.write({'status': 200, 'msg': result['msg'], 'links': result['links']})


class FilesSharingListHandler(BaseHandler):
    """003查看分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        print self.session.set('sharing', 'aa')
        result = files_libs.files_sharing_list_lib(self, uu)
        if result['status'] is True:
            kw = {'files': result['data'], 'uuid': result['uuid']}
            return self.render('files/files_sharing_list.html', **kw)
        return self.write(result['msg'])


class FilesSaveSharingHandler(BaseHandler):
    """004保存分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = files_libs.save_sharing_files_lib(self, uu)
        if result['status'] is True:
            return self.redirect('/files/files_page_list/1')
        return self.write(result['msg'])

#-----------------------------分享链接处理器-------------------------------

class FilesUploadQiniuHandler(BaseHandler):
    """03文件上传到七牛服务器"""
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = files_libs.upload_files_qiniu_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了','data': result})


class FilesDownLoadQiniuHandler(BaseHandler):
    """04从七牛服务器下载文件"""
    def get(self):
        uuid =self.get_argument('uuid', '')
        result = files_libs.files_download_qiniu_lib(self, uuid)
        if result['status'] is True:
            return self.redirect(result['data'])
        else:
            return self.write(result['msg'])


import tornado.gen
# 线程值
from concurrent.futures import ThreadPoolExecutor
executor_g = ThreadPoolExecutor(50)


#重点掌握（异步函数，异步下载器）
class FilesDownLoadHandler(BaseHandler):
    executor = executor_g # 赋予类的属性
    @tornado.gen.coroutine # 异步下载装饰器
    def get(self):
        uuid = self.get_argument('uuid', '')
        yield files_libs.files_download_lib(self, uuid)

     # yield是生成器





