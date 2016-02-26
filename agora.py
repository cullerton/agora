import transaction

from .models import Idea, Author
from .exceptions import *

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from logging import getLogger
logger = getLogger(__name__)

authors_limit = 5
ideas_limit = 5


class AgoraBase():

    # def _get_item_count(self, table):
    #     try:
    #         item_count = self.session.query(table).count()
    #     except:
    #         raise

    #     return item_count

    def _get_item_by_id(self, table, id):
        try:
            result = self.session.query(table).filter_by(id=id).one()
        except NoResultFound:
            raise InvalidItem

        return result

    def _get_item_by_filter(self, table, **filters):
        try:
            result = self.session.query(table).filter_by(**filters).one()
        except NoResultFound:
            raise
        except MultipleResultsFound:
            raise
        return result

    def _get_items(self, table, limit):
        items = []
        rows = self.session.query(table).order_by(table.created).limit(limit)
        for row in rows:
            items.append(row)
        return items

    def _get_items_by_filter(self, table, **filters):
        pass

    def _add_item(self, table, filters, **kwargs):
        with transaction.manager:
            new_item = table(**kwargs)
            self.session.add(new_item)
        try:
            item = self.session.query(table).filter_by(**filters).one()
        except:
            raise AddItem
        return item.id

    def _delete_item(self, table, id):
        with transaction.manager:
            try:
                self.session.query(table).filter_by(id=id).one()
            except NoResultFound:
                raise InvalidItem
            else:
                self.session.query(table).filter_by(id=id).delete(
                    synchronize_session='fetch')

        try:
            self._get_item_by_id(table, id)
        except:
            # delete worked
            return id
        else:
            # idea is still in the database, so delete failed
            raise DeleteItem


class Agora(AgoraBase):

    """python 'api' to database of ideas
       ideas have an author"""

    def __init__(self, session):
        """add the SQLAlchemy database session"""
        self.session = session
        self.authors_limit = authors_limit
        self.ideas_limit = ideas_limit

    #
    # Authors
    #

    def get_authors(self, limit=5):
        if not isinstance(limit, int) or limit < 0:
            limit = self.authors_limit

        try:
            authors = self._get_items(Author, limit)
        except Exception as e:
            logger.info("get_authors: except: e: %s" % e)
            raise
        logger.info("get_authors: type(authors): %s " % type(authors))
        return authors

    def get_author(self, id):
        try:
            author = self._get_item_by_id(Author, id)
        except:
            return InvalidAuthor

        return author

    def add_author(self, username, fullname, email):
        filters = {'username': username}
        kwargs = {'username': username, 'fullname': fullname, 'email': email}

        # check whether the author already exists
        try:
            self._get_item_by_filter(Author, **filters)
        except NoResultFound:
            # the author does not already exist, we can attempt to add it below
            pass
        else:
            # the author already exists
            raise DuplicateAuthor

        # the author does not already exist, attempt to add the author
        try:
            new_author_id = self._add_item(Author, filters, **kwargs)
        except:
            raise AddAuthor

        return new_author_id

    def edit_author(self, id, **kwargs):
        """edit an author already in the database"""
        with transaction.manager:
            author = self.session.query(Author).filter_by(id=id).one()
            for (key, value) in kwargs.items():
                if hasattr(author, key):
                    try:
                        setattr(author, key, value)
                    except:
                        raise EditAuthor
        test_author = self.session.query(Author).filter_by(id=id).one()
        return test_author.id

    def delete_author(self, id):
        """delete an idea from the database"""

        try:
            self._delete_item(Author, id)
        except DeleteItem:
            raise DeleteAuthor
        except InvalidItem:
            raise InvalidAuthor
        return id

    #
    # Ideas
    #

    def get_ideas(self, limit=5):
        """list of most recent ideas"""
        if not isinstance(limit, int) or limit < 0:
            limit = self.ideas_limit

        try:
            ideas = self._get_items(Idea, limit)
        except Exception as e:
            logger.info("get_ideas: except: e: %s" % e)
            raise e
        return ideas

    def get_idea(self, id):
        """return the requested idea"""
        try:
            idea = self._get_item_by_id(Idea, id)
        except InvalidItem:
            raise InvalidIdea

        return idea

    def add_idea(self, title, idea, author_id):
        """add an idea to the database
           return id of new entry
           return DuplicateIdea if idea already exists
           return AddIdea if an error occurs"""

        try:
            author = self._get_item_by_id(Author, author_id)
        except InvalidItem:
            raise InvalidAuthor
        filters = {'title': title}
        kwargs = {'title': title,
                  'idea': idea,
                  'author': author,
                  }

        # check whether the idea already exists
        try:
            self._get_item_by_filter(Idea, **filters)
        except NoResultFound:
            # the idea does not already exist, we can attempt to add it below
            pass
        else:
            # the idea already exists
            raise DuplicateIdea

        # the idea does not already exist, attempt to add the idea
        try:
            new_idea_id = self._add_item(Idea, filters, **kwargs)
        except InvalidItem:
            raise InvalidIdea
        except Exception as e:
            logger.info("add_idea: Exception: %s" % str(e))
            raise

        return new_idea_id

    def edit_idea(self, id, **kwargs):
        """edit an idea already in the database"""
        with transaction.manager:
            idea = self.session.query(Idea).filter_by(id=id).one()
            for (key, value) in kwargs.items():
                logger.info("edit_idea: key: %s, value: %s " % (key, value))
                if hasattr(idea, key):
                    try:
                        setattr(idea, key, value)
                    except:
                        # not sure what we'll ultimately do here
                        return EditIdea
        test_idea = self.session.query(Idea).filter_by(id=id).one()
        return test_idea.id

    def delete_idea(self, id):
        """delete an idea from the database"""

        try:
            result = self._delete_item(Idea, id)

        except InvalidItem:
            # not sure what we'll ultimately do here
            return InvalidIdea

        except DeleteItem:
            # not sure what we'll ultimately do here
            return DeleteIdea

        # result should be the same as id
        return result

__all__ = ['Agora']
