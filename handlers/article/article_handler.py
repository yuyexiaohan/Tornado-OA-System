# coding=utf-8 
# @Time : 2018/8/6 20:47 
# @Author : achjiang
# @File : article_handler.py
import json
from handlers.base.base_handler import BaseHandler
from libs.article import article_libs


class ArticleListHandler(BaseHandler):
	'''文章列表'''
	def get(self):
		# 将前端需要的变量拿过来定义
		articles,comments,categorys,tags =  article_libs.article_list_lib(self)
		kw = {
			'articles': articles,
			'newarticles': articles[:3],
			'newcomments': comments[:3],
			'categorys': categorys,
			'tags': tags,
		}
		# 返回一个html文件，并将定义的变量传到该模板
		self.render('article/article_list.html',**kw)


class AddArticleHandler(BaseHandler):
	'''添加文章'''
	def get(self):
		tags,categorys = article_libs.get_tags_categorys_lib(self)
		kw = {'tags': tags, 'categorys': categorys}
		self.render('article/add_article.html',**kw)

	def post(self):
		title = self.get_argument('title','')
		article = self.get_argument('article','')
		desc = self.get_argument('desc','')
		category = self.get_argument('category','')
		thumbnail = self.get_argument('thumbnail','')
		tags = json.loads(self.get_argument('tags','')) # 使用json让tags序列化

		article_id = self.get_argument ('article_id', '')

		print title,article,desc,category,thumbnail,tags

		result = article_libs.add_article_lib(self,title,article,desc,category,thumbnail,tags,article_id)
		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write ({'status': 400, 'msg': result['msg']})


class ArticleHandler(BaseHandler):
	'''文章详情栏'''
	def get(self):
		article_id = self.get_argument ('id', '')
		article,comments = article_libs.article_lib(self,article_id)
		kw = {'article':article,'comments':comments}
		self.render('article/article.html',**kw)



class AddCommentHandler(BaseHandler):
	'''添加评论'''
	def get(self):
		pass

	def post(self):
		content = self.get_argument('content','')
		article_id = self.get_argument('id','')

		result = article_libs.add_comment_lib(self,content,article_id)

		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write ({'status': 400, 'msg': result['msg']})



class AddSecondCommentHandler(BaseHandler):
	'''二级评论'''
	def post(self):
		content = self.get_argument('content','')
		comment_id = self.get_argument('id','')

		result = article_libs.add_second_comment_lib(self,content,comment_id)

		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write ({'status': 400, 'msg': result['msg']})


class AddLikeHandler(BaseHandler):
	'''点赞'''
	def post(self):
		article_id = self.get_argument ('article_id', '')

		result = article_libs.add_like_lib(self,article_id)

		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write ({'status': 400, 'msg': result['msg']})

class ArticleModifyManageHandler(BaseHandler):
	'''文章管理'''
	def get(self):
		articles = article_libs.articles_modify_list_lib()
		kw = {'articles':articles}

		self.render('article/article_modify_manage.html',**kw)


class ArticleModifyHandler(BaseHandler):
	'''编辑文章'''
	def get(self):
		article_id = self.get_argument('id','')

		article,tags,categorys = article_libs.get_article_tags_categorys_lib(self,article_id)
		kw = {'article': article,'tags': tags,'categorys': categorys,
		}
		self.render('article/article_modify.html',**kw)

	# 编辑使用的ajax请求，未使用post请求
	def post(self):
		pass


class ArticleDeleteHandler(BaseHandler):
	'''删除文章'''
	def get(self):
		article_id = self.get_argument('id','')
		articles = article_libs.article_delete_lib(self,article_id)
		kw = {'articles':articles}
		self.render('article/article_modify_manage.html',**kw)


class AddCategoryTagListHandler(BaseHandler):
	'''添加标签及分类'''
	def get(self):
		tags, categorys = article_libs.add_tags_categorys_list_lib(self)
		kw ={ 'tags':tags,'categorys':categorys }
		return self.render('article/article_add_category_tag.html',**kw)

	def post(self):
		category_name = self.get_argument('category_name','')
		tag_name = self.get_argument('tag_name','')
		result = article_libs.add_tags_categorys_lib(self,category_name,tag_name)
		if result['status'] is True:
			return self.write({'status':200,'msg':result['msg']})
		return self.write ({'status': 400, 'msg': result['msg']})


class DeleteCategoryTagHandler(BaseHandler):
	'''删除分类和标签'''
	def get(self):
		c_uuid = self.get_argument ('c_uuid', '')
		t_uuid = self.get_argument ('t_uuid', '')
		tags, categorys = article_libs.delete_tags_categorys_lib(self,c_uuid,t_uuid)
		kw ={ 'tags':tags,'categorys':categorys }
		return self.render('article/article_add_category_tag.html',**kw)

class SearchHandler(BaseHandler):
	'''查询'''
	def get(self):
		category_id = self.get_argument('category_id','')
		tag_id = self.get_argument('tag_id','')

		articles,comments,categorys,tags =  article_libs.article_search_list_lib(self,category_id,tag_id)
		kw = {
			'articles': articles,
			'newarticles': articles[:3],
			'newcomments': comments[:3],
			'categorys': categorys,
			'tags': tags,
		}
		# 返回一个html文件，并将定义的变量传到该模板
		self.render('article/article_list.html',**kw)


