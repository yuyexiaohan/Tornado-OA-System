#coding=utf-8
from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession


class UserLikeArticle(Base):
    """点赞表"""
    __tablename__ = 'article_user_like'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    article_id = Column(Integer, ForeignKey('article_article.id'), nullable=False, primary_key=True)


class ArticleToTag(Base):
    """标签与文章关系表"""
    __tablename__ ='article_to_tag'
    article_id = Column(Integer, ForeignKey('article_article.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('article_tag.id'), primary_key=True)


class SecondComment(Base):
    """二级评论"""
    __tablename__ = 'article_second_comment'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = Column(Text)
    createtime = Column(DateTime, index=True, default=datetime.now)
    #与文章表建立外键关系
    comment_id = Column(Integer, ForeignKey('article_comment.id', ondelete="CASCADE"))
    #与用户表建立外键关系
    user_id = Column(Integer, ForeignKey('user.id'))


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

class Comment(Base):
    """评论表"""
    __tablename__ = 'article_comment'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = Column(Text)
    createtime = Column(DateTime, index=True, default=datetime.now)
    #与文章表建立外键关系
    article_id = Column(Integer, ForeignKey('article_article.id', ondelete="CASCADE"))
    #与用户表建立外键关系
    user_id = Column(Integer, ForeignKey('user.id'))

    # 建立orm查询关系,评论表与二级评论表的一对多关系
    second_comments = relationship('SecondComment', backref='comment', order_by=-SecondComment.createtime)

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

    @classmethod
    def all_createtime_desc(cls):
        return dbSession.query(cls).order_by(cls.createtime.desc()).all()

class Article(Base):
    """文章表"""
    __tablename__ = 'article_article'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    title = Column(String(50))
    desc = Column(Text)
    thumbnail = Column(Text)
    readnum = Column(Integer, default=0)
    content = Column(Text)
    createtime = Column(DateTime, index=True, default=datetime.now)

    # 与用户建立外键关系
    user_id = Column(Integer, ForeignKey('user.id'))

    #与分类建立外键关系，加入ondelete="CASCADE"关联，当category删除时，文章也会被删除
    category_id = Column(Integer, ForeignKey('article_category.id',ondelete="CASCADE"))

    # 建立orm查询关系,文章表与评论表的一对多关系
    # 加入passive_deletes = True 表面Article下的字表comments表可以删除，
    # 但实际删除还是需要引入Comment表中与文章的外键关联中加入级联删除：ondelete="CASCADE"(这条命令是副表被删除，这个部分也被删除)
    # 二级评论中的数据也是按照这个方式进行操作删除文章中对应的评论关联表
    comments = relationship('Comment', backref='article', passive_deletes=True, order_by=-Comment.createtime)

    # 建立orm查询关系,标签表与文章表的多对多关系
    tags = relationship('Tag', secondary=ArticleToTag.__table__)

    #建立orm查询关系，用户表与文章表多对多的点赞关系
    user_likes=relationship('User', secondary=UserLikeArticle.__table__)



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

    @classmethod
    def all_createtime_desc(cls):
        return dbSession.query(cls).order_by(cls.createtime.desc()).all()


class Category(Base):
    """分类表"""
    __tablename__ = 'article_category'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True,  default=lambda:str(uuid4()))
    name = Column(String(50), unique=True, default='未分类')
    createtime = Column(DateTime, index=True, default=datetime.now)

    # 建立orm查询关系,分类表与文章表的一对多关系
    articles = relationship('Article', backref='category')

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


class Tag(Base):
    """标签表"""
    __tablename__ = 'article_tag'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True,  default=lambda:str(uuid4()))
    name = Column(String(50), unique=True,default='无标签' )
    createtime = Column(DateTime, index=True, default=datetime.now)

    #建立orm查询关系,标签表与文章表的多对多关系
    articles=relationship('Article', secondary=ArticleToTag.__table__)

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




