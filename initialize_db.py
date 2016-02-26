import os
import sys
import transaction

from sqlalchemy import create_engine

from .models import Idea, Author, Base

from . import DBSession


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <database_uri>\n'
          '(example: "%s sqlite:///:memory:")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    database_uri = argv[1]
    engine = create_engine(database_uri)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        author = Author(username='michaelc', fullname='mike cullerton',
                        email='michaelc@cullerton.com')
        DBSession.add(author)
    with transaction.manager:
        author = DBSession.query(Author).filter_by(username='michaelc').one()
        idea = Idea(title='First Idea!', idea='This is my idea.',
                    author=author)
        DBSession.add(idea)
        idea = Idea(title='Another Idea!', idea='This is another idea.',
                    author=author)
        DBSession.add(idea)
