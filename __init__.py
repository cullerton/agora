from .agora import Agora
from .models import Author
from .models import Base
from .models import Idea

from pyramid.config import Configurator
from pyramid.renderers import JSON

from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

__all__ = ['Agora', 'Idea', 'Author', 'DBSession', 'Base']


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    json_renderer = JSON()

    config = Configurator(settings=settings)
    config.add_renderer(None, json_renderer)
    config.add_route('view_idea', '/ideas/{idea}', request_method='GET')
    config.add_route('edit_idea', '/ideas/{idea}', request_method='PUT')
    config.add_route('delete_idea', '/ideas/{idea}', request_method='DELETE')
    config.add_route('list_ideas', '/ideas', request_method='GET')
    config.add_route('add_idea', '/ideas', request_method='POST')
    config.scan()
    return config.make_wsgi_app()
