#coding=utf-8
'''
This module is for internal use, only. It contains datastore drivers to be used
with the session and notification managers.
'''
from copy import copy
import pickle


class Driver(object):
    """
    只保留通用的属性和方法
    不通用的需要子类继承
    """
    EXPIRE_SECONDS = 24 * 60 * 60

    client = None

    def _to_dict(self, raw_session):
        """pickle字符串转字典"""
        if raw_session is None:
            return {}
        else:
            return pickle.loads(raw_session)

    def _setup_client(self):
        """创建链接，如果是空就创建，如果已经创建就不用在创建了"""
        if self.client is None:
            self._create_client()

    def get(self, session_id):
        """获取session_id"""
        self._setup_client()
        raw_session = self.client.get(session_id)

        return self._to_dict(raw_session)



    def set(self, session_id, session):
        """保存seesion,pickle字典到字符串"""
        print "session_id是redis中的键------%s" % session_id
        print "session内容------%s" % session
        #{'4780de42-8618-487a-be16-0f503240df99':{'user': u'111'}}
        pickled_session = pickle.dumps(session)
        #创建客户端链接
        self._setup_client()
        #向redis中保存数据和设置过期时间
        self._set_and_expire(session_id, pickled_session)


class RedisDriver(Driver):
    DEFAULT_STORAGE_IDENTIFIERS = {
        'db_sessions': 0,
        'db_notifications': 1,
    }

    def __init__(self, settings):
        self.settings = settings

    def _set_and_expire(self, session_id, pickled_session):
        """向redis中保存数据"""
        self.client.set(session_id, pickled_session)
        self.client.expire(session_id, self.EXPIRE_SECONDS)


    def _create_client(self):
        """创建客户端"""
        import redis
        if 'max_connections' in self.settings:
            #如果有最大链接池参数，创建个连接池
            connection_pool = redis.ConnectionPool(**self.settings)
            #更新配置参数
            settings = copy(self.settings)
            del settings['max_connections']
            settings['connection_pool'] = connection_pool
        else:
            settings = self.settings
        #增加一个self.client属性，第一次使用的时候创建
        self.client = redis.Redis(**settings)


class MemcachedDriver(Driver):
    def __init__(self, settings):
        self.settings = settings

    def _set_and_expire(self, session_id, pickled_session):
        self.client.set(session_id, pickled_session, self.EXPIRE_SECONDS)

    def _create_client(self):
        import memcache
        settings = copy(self.settings)
        default_servers = ('localhost:11211',)
        servers = settings.pop('servers', default_servers)
        self.client = memcache.Client(servers, **settings)


class DriverFactory(object):
    STORAGE_CATEGORIES = ('db_sessions', 'db_notifications')

    def create(self, name, storage_settings, storage_category):
        #name 是配置文件中的'engine':'redis'
        #self是DriverFactory自己，获取自己的类方法中的'_create_redis'方法
        method = getattr(self, '_create_%s' % name, None)
        if method is None:
            raise ValueError('Engine "%s" is not supported' % name)
        #如果有这个方法就执行并传入配置参数，和'db_sessions'
        return method(storage_settings, storage_category)
        #self._create_redis(storage_settings, storage_category)

    def _create_redis(self, storage_settings, storage_category):
        storage_settings = copy(storage_settings)
        #default_storage_identifier=0
        default_storage_identifier = RedisDriver.DEFAULT_STORAGE_IDENTIFIERS[storage_category]
        #如果不传入数据库 默认数据库为0
        storage_settings['db'] = storage_settings.get(storage_category, default_storage_identifier)
        for storage_category in self.STORAGE_CATEGORIES:
            if storage_category in storage_settings.keys():
                #删掉'db_sessions':,
                del storage_settings[storage_category]
        #返回创建的RedisDriver实例
        return RedisDriver(storage_settings)

    def _create_memcached(self, storage_settings, storage_category):
        return MemcachedDriver(storage_settings)
