##coding=utf-8
'''
This module contains SessionMixin, which can be used in RequestHandlers, and
SessionManager, which is the real session manager, and is referenced by the
SessionMixin.

It's mandatory that you set the "cookie_secret" in your application settings,
because the session ID is stored in a secure manner. It's also mandatory that
you have a "pycket" dictionary containing at least an "engine" element that
tells which engine you want to use.

Supported engines, for now, are:
- Redis
- Memcache

If you want to change the settings that are passed to the storage client, set a
"storage" dictionary in the "pycket" settings with the intended storage settings
in your Tornado application settings. When you're using Redis, all these
settings are passed to the redis.Redis client, except for the "db_sessions" and
"db_notifications". These settings can contain numbers to change the datasets
used for persistence, if you don't want to use the default numbers.

If you want to change the cookie settings passed to the handler, set a
"cookies" setting in the "pycket" settings with the items you want.
This is also valid for "expires" and "expires_days", which, by default, will be
None, therefore making the sessions expire on browser close, but, if you set one
of them, your custom value will override the default behaviour.
'''

from uuid import uuid4

from driver import DriverFactory


class SessionManager(object):

    '''
    This is the real class that manages sessions. All session objects are
    persisted in a Redis or Memcache store (depending on your settings).
    After 1 day without changing a session, it's purged from the datastore,
    to avoid it to grow out-of-control.

    When a session is started, a cookie named 'PYCKET_ID' is set, containing the
    encrypted session id of the user. By default, it's cleaned every time the
    user closes the browser.

    The recommendation is to use the manager instance that comes with the
    SessionMixin (using the "session" property of the handler instance), but it
    can be instantiated ad-hoc.
    '''

    SESSION_ID_NAME = 'PYCKET_ID'
    STORAGE_CATEGORY = 'db_sessions'

    driver = None

    def __init__(self, handler):
        '''
        Expects a tornado.web.RequestHandler
        初始化时传入RequestHandler
        初始化工厂类
        '''
        print '-----------------session.__init__-------------'
        self.handler = handler
        self.settings = {}
        self.__setup_driver()

    def __setup_driver(self):
        """
        通过配置文件和工厂模式创建redis或memcached
        """
        #获得配置信息
        self.__setup_settings()
        #获得数据库配置信息
        storage_settings = self.settings.get('storage', {})
        #实例化工厂类
        factory = DriverFactory()
        #通过传入的参数创建相应的数据库实例
        self.driver = factory.create(self.settings.get('engine'), storage_settings, self.STORAGE_CATEGORY)

    def __setup_settings(self):
        """
        获取app中的settings配置信息
        """
        pycket_settings = self.handler.settings.get('pycket')
        if not pycket_settings:
            raise ConfigurationError('The "pycket" configurations are missing')
        engine = pycket_settings.get('engine')
        #'redis'
        if not engine:
            raise ConfigurationError('You must define an engine to be used with pycket')
        self.settings = pycket_settings

    def set(self, name, value):
        '''
        Sets a value for "name". It may be any pickable (see "pickle" module
        documentation) object.
        为使用者提供的设置接口
        通过键和值设置session
        '''

        def change(session):
            session[name] = value
        self.__change_session(change)

    def get(self, name, default=None):
        '''
        Gets the object for "name", or None if there's no such object. If
        "default" is provided, return it if no object is found.
        为使用者提供的获取接口
        通过键获取session 值，如果获取不到返回None
        '''

        session = self.__get_session_from_db()
        #如果找不到session,返回空值
        return session.get(name, default)

    def delete(self, *names):
        '''
        Deletes the object with "name" from the session, if exists.
        删除sassion
        '''

        def change(session):
            """一个回调函数"""
            keys = session.keys()
            #获取列表，遍历names得到name，如果name在keys里向列表添加name元素
            names_in_common = [name for name in names if name in keys]
            for name in names_in_common:
                del session[name]
        #修改session
        self.__change_session(change)
    #__delitem__(self,key):删除给定键对应的元素
    __delitem__ = delete

    def keys(self):
        """
        查看所有的键
        """
        session = self.__get_session_from_db()
        return session.keys()

    def iterkeys(self):
        """
        可以对键进行迭代
        """
        session = self.__get_session_from_db()
        return iter(session)
    __iter__ = iterkeys

    def __getitem__(self, key):
        """__getitem__(self,key):返回键对应的值。"""
        value = self.get(key)
        if value is None:
            raise KeyError('%s not found in session' % key)
        return value

    def __setitem__(self, key, value):
        """__setitem__(self,key,value)：设置给定键的值"""
        self.set(key, value)

    def __contains__(self, key):
        """__contains__(self, key):当使用in，not in 对象的时候"""
        session = self.__get_session_from_db()
        return key in session

    def __set_session_in_db(self, session):
        """设置session到数据库"""
        session_id = self.__get_session_id()
        #调用driver的set方法保存session
        self.driver.set(session_id, session)


    def __get_session_from_db(self):
        """
        从数据库中获取session
        """
        #先到cookie中获取session_id
        session_id = self.__get_session_id()
        # 根据uuid的session_id值，调用driver的get方法获取保存的键值对
        return self.driver.get(session_id)

    def __get_session_id(self):
        """
        获取session_id,通过handler的get_secure_cookie方法，
        SESSION_ID_NAME = 'PYCKET_ID'
        如果cookie中已经存在了session_id，就返回session_id
        """
        session_id = self.handler.get_secure_cookie(self.SESSION_ID_NAME)
        if session_id is None:
            #获取不到就创建一个session_id,创建的时候保存在cookie中
            session_id = self.__create_session_id()
        return session_id

    def __create_session_id(self):
        """创建一个session_id"""
        session_id = str(uuid4())
        #4780de42-8618-487a-be16-0f503240df99
        #设置secure_cookie,键是'PYCKET_ID'值是uuid4的随机字符串，
        self.handler.set_secure_cookie(self.SESSION_ID_NAME, session_id,
                                       **self.__cookie_settings())
        return session_id

    def __change_session(self, callback):
        """
        修改session
        """
        session = self.__get_session_from_db()
        callback(session)
        self.__set_session_in_db(session)

    def __cookie_settings(self):
        """从setting 中的cookies获取有效期"""
        cookie_settings = self.settings.get('cookies', {})
        print '从cookie_settiongs中获取有效期-------', cookie_settings
        cookie_settings.setdefault('expires', None)
        cookie_settings.setdefault('expires_days', None)
        return cookie_settings


class SessionMixin(object):
    '''
    This mixin must be included in the request handler inheritance list, so that
    the handler can support sessions.

    Example:
    >>> class MyHandler(tornado.web.RequestHandler, SessionMixin):
    ...    def get(self):
    ...        print type(self.session) # SessionManager

    Refer to SessionManager documentation in order to know which methods are
    available.
    '''

    @property
    def session(self):
        '''
        Returns a SessionManager instance
        '''
        return create_mixin(self, '__session_manager', SessionManager)
    #self.session.get('username')

class ConfigurationError(Exception):
    pass


def create_mixin(context, manager_property, manager_class):
    """
    :param context: 是requesthandler
    :param manager_property: 是'__session_manager'字符串
    :param manager_class: 是SessionManager
    :return:
    """
    #创建SessionManager类，并传入requesthandler
    # hasattr用法：hasattr(对象，属性字符串）
    if not hasattr(context, manager_property):
        #setattr用法：setattr(对象，属性，属性的值)
        setattr(context, manager_property, manager_class(context))
    #getattr用法：getattr(对象，属性字符串）
    return getattr(context, manager_property)