#coding=utf-8
from uuid import uuid4
from datetime import datetime
from string import printable

from pbkdf2 import PBKDF2

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession

from models.permission.permission_model import UserToRole
from models.files.upload_file_model import FilesToUser,DelFilesToUser


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String(50), nullable=False)

    # 变量名前加'_'是说明这个变量是不能直接访问的，需要通过下面
    # 定义的类来访问，即所谓'私有变量'
    _password = Column('password', String(64), nullable=False)
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)

    # 登录数量
    loginnum = Column(Integer, default=0)
    # 锁，锁定用户
    _locked = Column(Boolean, default=False, nullable=False)
    # 图像的存储路径
    _avatar = Column(String(64))
    # 逻辑删除，并不是删除实际的用户数据，指示给一个标志，代表数据已删除
    _isdelete = Column(Boolean, default=False, nullable=False)

    email = Column(String(50))
    mobile = Column(String(50))
    # ？
    num = Column(String(50), unique=True)
    qq = Column(String(50))


    #角色表和用户表多对多查询关系
    # 需要属性SQLalchemy数据库和表关系
    # users = relationship("User", secondary=UserToRole.__table__) # role表对应user表的关系句子
    # 关联表变量=relationship("关联表名"，secondary=当前表面To关联表名.__table__)
    roles = relationship("Role", secondary=UserToRole.__table__)
    # 建立article与user的关联表关系，这样在article中就可以调用user信息
    article = relationship("Article", backref = 'user')
    # 建立comments与user的关联表关系，这样在comments中就可以调用user信息
    comments = relationship("Comment", backref = 'user')

    second_comments = relationship("SecondComment", backref = 'user')

    # 关联文件表和用户
    users_files = relationship ("Files", secondary=FilesToUser.__table__, lazy='dynamic')
    # 关联文件删除表和用户
    users_files_del = relationship ("Files", secondary=DelFilesToUser.__table__)


    @classmethod
    # """类装饰器"""
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(name=name).first()

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        print self._hash_password(password)
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @property
    def avatar(self): #取值
        return self._avatar if self._avatar else "default_avatar.jpeg" # 默认图像命名


    @avatar.setter #赋值
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data) # 可以返回一个文件扩展名
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):
                    os.unlink("static/images/useravatars/" + self._avatar)
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)

                # 打开一个文件，并肩文件赋一个值，并将它以一个名字命名
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext

            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        """把数据导成一个字典结构"""
        return {
            'id': self.id,
            'name': self.name,
            'last_login': self.last_login,
        }
