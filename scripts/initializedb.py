import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Idea,
    Category,
    Tag,
    IdeaTag,
    Base,
)

from logging import getLogger
logger = getLogger(__name__)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def seed_categories():
    for name in ['Local', 'Politics', 'Sports']:
        logger.info("len(query): %s" % str(len(
            DBSession.query(Category).filter_by(name=name).all())))
        if len(DBSession.query(Category).filter_by(name=name).all()) == 0:
            with transaction.manager:
                model = Category(name=name)
                DBSession.add(model)


def seed_tags():
    for name in ['Python', 'Zoey', 'BBQ']:
        # if not DBSession.query(Tag).filter(Tag.name=name):
        if len(DBSession.query(Tag).filter_by(name=name).all()) == 0:
            with transaction.manager:
                model = Tag(name=name)
                DBSession.add(model)


def seed_ideas():
    if len(DBSession.query(Idea).filter_by(id='first-post').all()) == 0:
        with transaction.manager:
            model = Idea(id='first-post',
                         title='First Post!',
                         intro="This is my first post",
                         body="I was about to say something...",
                         parent=0,
                         category_id=1,
                         created=None,
                         modified=None
                         )
            DBSession.add(model)

    if len(DBSession.query(IdeaTag).filter_by(
            idea_id='first-post', tag_id=1).all()) == 0:
        with transaction.manager:
            model = IdeaTag(idea_id='first-post', tag_id=1)
            DBSession.add(model)

    if len(DBSession.query(Idea).filter_by(id='second-post').all()) == 0:
        with transaction.manager:
            model = Idea(id='second-post',
                         title='Second Post!',
                         intro="This is my second post",
                         body="I thought there was something to say...",
                         parent=0,
                         category_id=2,
                         created=None,
                         modified=None
                         )
            DBSession.add(model)

    if len(DBSession.query(IdeaTag).filter_by(
            idea_id='second-post', tag_id=2).all()) == 0:
        with transaction.manager:
            model = IdeaTag(idea_id='second-post', tag_id=2)
            DBSession.add(model)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    seed_categories()
    seed_tags()
    seed_ideas()
