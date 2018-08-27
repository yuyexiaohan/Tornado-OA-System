#coding=utf-8
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.escape
from tornado.options import define, options
from config import settings
from handlers.main.main_urls import handlers
# from models.account.account_user_model import User
# from models.files.upload_file_model import Files
# from models.article import article_model
from libs.db import create_talbes
from libs.db.dbsession import dbSession
from models.account.account_user_model import User # 引入User表,编辑在改文件下的option.t创建表
from models.permission.permission_model import (Role,Permission,PermissionToRole,UserToRole,Handler,Menu)
from models.article.article_model import (Article,ArticleToTag,UserLikeArticle,Comment,Category,SecondComment,Tag)
# 这里不导入表，就无法创建
from models.files.upload_file_model import FilesToUser,DelFilesToUser,Files


print 'dir(tornado):',dir(tornado)
print 'dir(tornado.web):',dir(tornado.web)
print 'dir(tornado.web.Application):',dir(tornado.web.Application)

#定义一个默认的端口
define("port", default=8000, help="run port ", type=int) # 定义端口号
define("runserver", default=False, help="start server", type=bool) # 启动服务
define("t", default=False, help="create table", type=bool) # 创建表
define("u", default=False, help="create user", type=bool) # 创建用户


if __name__ == "__main__":
    # option(所有已定义的选项都可以作为该对象的属性可用).解析在命令行上给出的所有选项
    # 即在命令行输入命令时进行解析
    options.parse_command_line()

    # 当是属性.t时，执行创建表函数
    if options.t:
        create_talbes.run()

    # 当是属性.u时，就是创建用户命令
    # 定义如果执行-u时，为创建一个用户
    if options.u:
        user = User() # 类的实例化
        user.name = 'achjiang' # 属性的实例化
        user.password = '123456' # 属性的实例化
        dbSession.add(user) # 在session中添加一个数据
        dbSession.commit() # 将添加的数据提交到数据库执行

    # 当是属性.runserver时，执行如下函数：
    if options.runserver:
        app = tornado.web.Application(handlers, **settings) #创建应用实例
        http_server = tornado.httpserver.HTTPServer(app) #通过应用实例创建服务器实例
        http_server.listen(options.port)  #监听8000端口
        print 'start server...'
        tornado.ioloop.IOLoop.instance().start() #启动服务器

