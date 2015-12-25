import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
    Sequence,
    Boolean,
    ForeignKey,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()

from logging import getLogger
logger = getLogger(__name__)


class Idea(Base):
    """"""
    __tablename__ = 'ideas'
    id = Column(Integer, Sequence('idea_id_seq'), primary_key=True)
    title = Column(Text, unique=True)
    idea = Column(Text)
    visible = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now())
    modified = Column(DateTime, default=datetime.datetime.now())
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="ideas")

    def __init__(self, title, idea):
        self.title = title
        self.idea = idea

    def __repr__(self):
        return "%s" % (self.title)

    def to_dict(self):
        return {'title': self.title, 'idea': self.idea, 'author': self.author}


class Author(Base):
    """"""
    __tablename__ = 'authors'
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    username = Column(Text, unique=True)
    fullname = Column(Text, default='Anonymous')
    email = Column(Text)
    active = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now())

    ideas = relationship("Idea", order_by=Idea.id, back_populates="author")

    def __init__(self, username, fullname, email):
        self.username = username
        self.fullname = fullname
        self.email = email

    def __repr__(self):
        return "%s, %s" % (self.fullname, self.created.strftime("%B %d, %Y")
                           if self.created else self.created)
