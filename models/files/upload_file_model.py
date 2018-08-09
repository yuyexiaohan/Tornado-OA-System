#coding=utf-8
import hashlib
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


class FilesToUser(Base):
    """文件与用户关系表"""
    __tablename__ ='files_to_user'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    files_id = Column(Integer, ForeignKey('files_files.id'), primary_key=True)


class DelFilesToUser(Base):
    """回收站文件与用户关系表"""
    __tablename__ ='files_to_user_del'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    files_id = Column(Integer, ForeignKey('files_files.id'), primary_key=True)


def hash_data(datas):
    """获取数据的哈希结果"""
    h = hashlib.sha1()
    h.update(datas)
    return h.hexdigest()


class Files(Base):
    """文件类"""
    __tablename__ = 'files_files'

    uuid = Column(String(100), unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(50), nullable=False)
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    viewnum = Column(Integer, default=0)
    content_length = Column(Integer)
    #user_id = Column(Integer, ForeignKey('user.id'))
    content_type = Column(String(50))
    # 文件的hash值，便于查询
    _file_hash = Column(String(50), nullable=False, unique=True)
    _locked = Column(Boolean, default=False, nullable=False)

    files_users = relationship('User', secondary=FilesToUser.__table__)

    files_users_del = relationship('User', secondary=DelFilesToUser.__table__)

    @classmethod
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


    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self, datas):
        self._file_hash = hash_data(datas)

    @classmethod
    def file_is_existed(cls, other_dates):
        other_dates_hash = hash_data(other_dates)
        return cls.by_hash(other_dates_hash)


    @classmethod
    def by_hash(cls, other_dates_hash):
        return dbSession.query(cls).filter_by(_file_hash=other_dates_hash).first()


    @classmethod
    def display_file_list(cls):
        return dbSession.query(cls).filter(cls._locked == False).all()


    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

