# coding=utf-8 
# @Time : 2018/8/6 21:05 
# @Author : achjiang
# @File : article_libs.py
from models.article.article_model import (Article,ArticleToTag,UserLikeArticle,Comment,Category,SecondComment,Tag)


def article_list_lib(self):
	'''赋值给前端模板数据'''
	articles = Article.all_createtime_desc()
	comments = Comment.all_createtime_desc()
	tags,categorys = get_tags_categorys_lib(self)
	return articles,comments,categorys,tags


def get_tags_categorys_lib(self):
	'''获取标签和分类'''
	tags = Tag.all()
	categorys = Category.all()
	return tags,categorys


def add_article_lib(self,title,content,desc,category_id,thumbnail,tags,article_id):
	'''发布新闻'''
	if category_id =='' or tags == '':
		return {'status':False,'msg':'请选择分类或者标签！'}

	if title == '' or content == '' or desc == '':
		return {'status':False,'msg':'请输入标题、内容、简介！'}

	# 判断文章是否存在，存在则是编辑，不存在则是新增
	if article_id != '':
		article = Article.by_id(article_id)
		article.tags = [] # 如果文章已存在，则避免标签重复，这里直接将标签置空
	else:
		article = Article()
	article.content = content
	article.title = title
	article.desc = desc
	article.category_id = category_id
	article.thumbnail = thumbnail

	for tags_id in tags:
		tag = Tag.by_id(tags_id)
		article.tags.append(tag)

	article.user_id = self.current_user.id
	self.db.add(article)
	self.db.commit()

	if article_id != '':
		return {'status': True, 'msg': '文档修改成功！'}
	return {'status':True,'msg':'文档提交成功！'}


def article_lib(self,article_id):
	'''文章详情'''
	article = Article.by_id(article_id)
	comment = article.comments
	return article,comment


def add_comment_lib(self,content,article_id):
	'''添加评论'''
	if content == '':
		return {'status': False, 'msg': '请输入评论！'}

	article = Article.by_id(article_id)
	if article is None:
		return {'status': False, 'msg': '文档不存在！'}

	comment = Comment()
	comment.content = content
	comment.article_id = article.id
	comment.user_id = self.current_user.id
	self.db.add(comment)
	self.db.commit()
	return {'status': True, 'msg': '评论成功！'}


def add_second_comment_lib(self,content,comment_id):
	'''二次评论'''
	if content == '':
		return {'status': False, 'msg': '请输入评论！'}

	comment = Comment.by_id(comment_id)
	if comment is None:
		return {'status': False, 'msg': '文档不存在！'}

	second_comment = SecondComment()
	second_comment.content = content
	second_comment.comment_id = comment.id
	second_comment.user_id = self.current_user.id
	self.db.add(second_comment)
	self.db.commit()
	return {'status': True, 'msg': '评论成功！'}


def add_like_lib(self,article_id):
	'''点赞'''
	if article_id is None:
		return {'status': False, 'msg': '文章不存在！'}

	article = Article.by_id(article_id)
	if article is None:
		return {'status': False, 'msg': '文章不存在！'}

	# 对当前用户是否存在user_like,存在执行取消点赞，不再执行点赞
	if self.current_user in article.user_likes:
		# 取消点赞
		article.user_likes.remove(self.current_user)
		self.db.add(article)
		self.db.commit()
		return {'status': True, 'msg': '取消点赞！'}

	# 点赞执行：
	article.user_likes.append(self.current_user)
	self.db.add(article)
	self.db.commit()
	return {'status': True, 'msg': '评论成功！'}


def articles_modify_list_lib():
	'''文章管理'''
	articles = Article.all()
	return articles

def get_article_tags_categorys_lib(self,article_id):
	'''文章编辑'''
	article = Article.by_id(article_id)
	tags, categorys = get_tags_categorys_lib(self)

	return article,tags,categorys


def article_delete_lib(self,article_id):
	'''删除文章'''
	article = Article.by_id(article_id)
	if article is None:
		return Article.all()
	self.db.delete(article)
	self.db.commit()
	# flash (self, '请输入角色名称！', 'error')
	return Article.all()


def add_tags_categorys_list_lib(self):
	'''添加标签和分类展示页面'''
	tags, categorys = get_tags_categorys_lib(self)
	return tags,categorys

def add_tags_categorys_lib(self,category_name,tag_name):
	'''管理标签'''
	if category_name != '':
		category = Category.by_name(category_name)
		if category is not None:
			return {'status': False, 'msg': '该分类名已存在！'}
		else:
			category = Category()
		category.name = category_name
		self.db.add(category)
		self.db.commit()
		return {'status':True,'msg':'分类添加成功！'}

	if tag_name != '':
		tag = Tag.by_name(tag_name)
		if tag is not None:
			return {'status': False, 'msg': '该分类名已存在！'}
		else:
			tag = Tag()
			tag.name = tag_name
		self.db.add(tag)
		self.db.commit()
		return {'status':True,'msg':'分类添加成功！'}
	return {'status': False, 'msg': '请添加分类或标签！'}


'''未级联删除，存在bug'''
def delete_tags_categorys_lib(self,c_uuid,t_uuid):
	'''删除分类和标签'''
	category = Category.by_uuid(c_uuid)
	tag = Tag.by_uuid (t_uuid)

	if category is None and tag is None:
		tags, categorys = get_tags_categorys_lib (self)
		return tags,categorys
	if category is not None:
		self.db.delete(category)
		self.db.commit()

	print 'tag：%s'%tag

	if tag is not None:
		self.db.delete(tag)
		self.db.commit()
	print 'test.....'
	tags, categorys = get_tags_categorys_lib(self)
	return tags,categorys






def article_search_list_lib(self,category_id,tag_id):
	'''查找'''
	if category_id != '':
		category = Category.by_id(category_id) # 获取分类
		articles = category.articles # 获取该分类的文章
	if tag_id != '':
		tag = Tag.by_id(tag_id) # 获取标签
		articles = tag.articles # 获取该标签的文章
	comments = Comment.all_createtime_desc() # 获取所有评论
	tags, categorys = get_tags_categorys_lib(self) # 获取标签和分类
	return articles,comments,categorys,tags # 返回这些参数赋值给handler







