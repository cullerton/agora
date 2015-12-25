import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from agora import (
    DBSession,
    Idea,
    Author,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        idea = Idea(title='First Idea!', idea='This is my idea.')
        DBSession.add(idea)
        idea = Idea(title='Another Idea!', idea='This is another idea.')
        DBSession.add(idea)
        author = Author(username='michaelc', fullname='mike cullerton',
                        email='michaelc@cullerton.com')
        DBSession.add(author)
