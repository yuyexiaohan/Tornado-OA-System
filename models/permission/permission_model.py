# coding=utf-8
# 权限管理列表
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


class Handler(Base):
    __tablename__ = 'permission_handler'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    p_id = Column(Integer, ForeignKey("permission_permission.id"))

    permission = relationship("Permission", uselist=False)

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


class Menu(Base):
    __tablename__ = 'permission_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    p_id = Column(Integer, ForeignKey("permission_permission.id"))

    permission = relationship("Permission", uselist=False)  # 要赋值一个Permission类对象

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


class PermissionToRole(Base):
    """权限角色多对多关系表"""
    __tablename__ = 'permission_to_role'
    p_id = Column(Integer, ForeignKey("permission_permission.id"), primary_key=True)
    r_id = Column(Integer, ForeignKey("permission_role.id"), primary_key=True)


class Permission(Base):
    """权限表"""
    __tablename__ = 'permission_permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    strcode = Column(String(50), nullable=False)  # 权限码

    roles = relationship("Role", secondary=PermissionToRole.__table__)

    menu = relationship("Menu", uselist=False)

    handler = relationship("Handler", uselist=False)

    # 建立orm查询关系，权限表文章表多对多的关系
    # permission_article = relationship('Article', secondary=ArticleToPermission.__table__)

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



class UserToRole(Base):
    """用户角色多对多关系表"""
    __tablename__="permission_user_to_role"
    u_id = Column(Integer, ForeignKey("user.id"), primary_key=True )
    r_id = Column(Integer, ForeignKey("permission_role.id"), primary_key=True)


class Role(Base):
    """角色表"""
    __tablename__ = 'permission_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    # 角色表和用户表多对多查询关系
    users = relationship("User", secondary=UserToRole.__table__)

    # 角色表和权限表多对多查询关系
    permissions = relationship("Permission", secondary=PermissionToRole.__table__)

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
