import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Tag(Base):
    """"""
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    
    def __init__(self, name):
        self.name = name
        
class Category(Base):
    """"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    
    def __init__(self, name):
        self.name = name
        
class Idea(Base):
    """"""
    __tablename__ = 'ideas'
    id = Column(Text, primary_key=True)
    title = Column(Text, unique=True)
    intro = Column(Text)
    body = Column(Text)
    parent = Column(Integer, ForeignKey("ideas.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, id, title, intro, body, parent, category_id, created, modified):
        self.id = id
        self.title = title
        self.intro = intro
        self.body = body
        self.parent = parent
        self.category_id = category_id
        self.created = created
        self.modified = modified


class IdeaTag(Base):
    """"""
    __tablename__ = 'idea_tags'
    __table_args__ = (UniqueConstraint('idea_id','tag_id'),)
    id = Column(Integer, primary_key=True)
    idea_id = Column(Text, ForeignKey("ideas.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    
    
    def __init__(self, idea_id, tag_id):
        self.idea_id = idea_id
        self.tag_id = tag_id
        
