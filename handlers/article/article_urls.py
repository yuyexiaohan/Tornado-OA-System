# coding=utf-8 
# @Time : 2018/8/6 20:47 
# @Author : achjiang
# @File : article_urls.py
import article_handler


article_urls = [
	(r'/article/article_list',article_handler.ArticleListHandler),
	(r'/article/add_article',article_handler.AddArticleHandler),
	(r'/article/article',article_handler.ArticleHandler),
	(r'/article/addcomment',article_handler.AddCommentHandler),
	(r'/article/addsecondcomment',article_handler.AddSecondCommentHandler),
	(r'/article/addlike',article_handler.AddLikeHandler),
	(r'/article/article_modify_manage',article_handler.ArticleModifyManageHandler),
	(r'/article/article_modify',article_handler.ArticleModifyHandler),
	(r'/article/article_delete',article_handler.ArticleDeleteHandler),
	(r'/article/add_category_tag_list',article_handler.AddCategoryTagListHandler),
	(r'/article/delete_category_tag',article_handler.DeleteCategoryTagHandler),
	(r'/article/search',article_handler.SearchHandler),
]