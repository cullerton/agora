from .models import (
    DBSession,
    Idea,
    )

from logging import getLogger
logger = getLogger(__name__)

from re import compile
_punct_re = compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

from sqlalchemy.sql import select
 
class agora_utils():
    """utility methods for Agora"""

    @staticmethod
    def slugify(text, delim=u'-'):
        """Generates an slightly worse ASCII-only slug.
           stolen from http://flask.pocoo.org/snippets/5/ and 
           http://stackoverflow.com/questions/9042515/normalizing-unicode-text-to-filenames-etc-in-python#
        """
        result = []
        for word in _punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result))

    @staticmethod
    def getIdeaById(id):
        """"""
        logger.info("getIdeaById: ")
        idea = DBSession.query(Idea).filter_by(id=id).one()
        return idea

    @staticmethod
    def getIdeasByDate(sort='asc', limit=None):
        """"""
        logger.info("getIdeasByDate: ")
        ideas = []
        s = select([Idea])
        for row in s.execute():
#         result = s.execute()
#         for row in result:
            ideas.append(row)
        return ideas

class Agora(object):

    """Agora - 
        a forum for community discussion"""

    # DBSession = DBSession

    @staticmethod
    def getIdeasByDate(sort='asc', limit=None):
        """"""
        logger.info("Agora: ")
        ideas = []
        s = select([Idea])
        result = s.execute()
        logger.info("Agora: result: %s" % str(result))
        for row in result:
            logger.info("Agora: row: %s" % str(row))
            ideas.append(row)
            
        logger.info("Agora: ideas: %s" % str(ideas))
        return ideas
