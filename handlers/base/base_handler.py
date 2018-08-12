#coding=utf-8
# 创建一个基类的handler
import tornado.escape
import tornado.web
import tornado.websocket
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_conn.redis_conn import conn #导入redis数据的连接
from models.account.account_user_model import User


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.flashes = None # 将弹框信息放入basehandler文件中，
        self.db = dbSession # 操作mysql数据库
        self.conn = conn # 操作redis数据库


    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name") # 从session中获取user.name
        user = None
        if username:
            user = User.by_name(username)
        # 如果用户存在，就返回user,如果不存在就返回None
        return user if user else None


    def on_finish(self):
        self.db.close()


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    def initialize(self):
        self.flashes = None # 将弹框信息放入basehandler文件中，
        self.db = dbSession # 操作mysql数据库
        self.conn = conn # 操作redis数据库


    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name") # 从session中获取user.name
        user = None
        if username:
            user = User.by_name(username)
        # 如果用户存在，就返回user,如果不存在就返回None
        return user if user else None


    def on_finish(self):
        self.db.close()

