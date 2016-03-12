from cullerton.agora.logging import logger
from cullerton.agora.models import Idea, Author
from cullerton.agora.exceptions import *

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

authors_limit = 5
ideas_limit = 5


class AgoraBase():

    def _validate_session(self):
        engine = self.session.get_bind()
        table_names = engine.table_names()
        try:
            assert 'ideas' in table_names and 'authors' in table_names
        except:
            raise InvalidSession

    def _session_query(self, table, filters={}, limit=None, order=None):
        """return result of query
           """
        try:
            result = self.session.query(
                table).filter_by(**filters).order_by(order).limit(limit)
        except Exception as e:
            logger.info("_session_query: Exception: %s" % str(e))
            pass
        else:
            return result

    def _get_item_count(self, table):
        """return count of items in table"""
        try:
            item_count = self._session_query(table).count()
        except:
            raise

        return item_count

    def _get_item(self, table, id):
        """return item identified by table and id"""
        filters = {'id': id}
        try:
            item = self._session_query(table, filters=filters).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise
        return item

    def _get_items(self, table, filters={}, limit=None, order=None):
        """return a list of items from table"""
        items = []
        result = self._session_query(
            table, filters=filters, limit=limit, order=order)
        for row in result:
            items.append(row)
        return items

    def _add_item(self, table, filters, **kwargs):
        """add an item to table with values in kwargs
                retreive new item with filters
           return new item id"""
        try:
            # 2 statements in a try :(
            new_item = table(**kwargs)
            self.session.add(new_item)
        except Exception as e:
            # swallow the Exception, we will fail below and raise AddItem
            logger.info("_add_item: Exception: %s" % str(e))
        else:
            self.session.commit()
        # try to get our new item
        try:
            item = self._session_query(table, filters).one()
        except NoResultFound:
            raise AddItem('No Result Found')
        return item.id

    def _delete_item(self, table, id):
        """return item from table"""
        # see if we have item
        filters = {'id': id}
        try:
            self._session_query(table, filters).one()
        except NoResultFound:
            raise InvalidItem
        else:
            # try to delete item
            try:
                # we cannot call .delete() on _session_query because order_by
                self.session.query(table).filter_by(id=id).delete()
            except Exception as e:
                logger.info("_delete_item: Exception: %s" % str(e))
            else:
                self.session.commit()

        # see if the delete worked
        try:
            self._session_query(table, filters).one()
        except NoResultFound:
            # delete worked
            return id
        else:
            # idea is still in the database, so delete failed
            raise DeleteItem

    def _edit_item(self, table, id, **kwargs):
        """edit an item"""
        filters = {'id': id}
        try:
            item = self._session_query(table, filters=filters).one()
        except (NoResultFound, MultipleResultsFound):
            raise
        else:
            for (key, value) in kwargs.items():
                if hasattr(item, key):
                    try:
                        setattr(item, key, value)
                    except:
                        raise EditItem
        return_item = self._session_query(table, filters=filters).one()
        return return_item.id


class Forum(AgoraBase):

    """a forum for ideas"""

    def __init__(self, session):
        """add the SQLAlchemy database session"""
        self.session = session
        self.authors_limit = authors_limit
        self.ideas_limit = ideas_limit
        self._validate_session()

    #
    # Authors
    #

    def get_author_count(self):
        return self._get_item_count(Author)

    def get_author(self, id):
        """return the requested author"""
        return self._get_item(Author, id)

    def get_authors(self, filters={}, limit=None, order=None):
        """return a list of authors
           with optional filters, limit, and order"""
        return self._get_items(
            Author, filters=filters, limit=limit, order=order)

    def add_author(self, username, fullname, email):
        if username:
            filters = {'username': username}
            kwargs = {'username': username, 'fullname': fullname, 'email': email}

            # check whether the author already exists
            if len(self._get_items(Author, filters=filters)) > 0:
                raise DuplicateAuthor

            # the author does not already exist, attempt to add the author
            try:
                new_author_id = self._add_item(Author, filters, **kwargs)
            except AddItem:
                raise AddAuthor

            return new_author_id
        else:
            raise AddAuthor

    def edit_author(self, id, **kwargs):
        """edit an author already in the database"""
        try:
            self._edit_item(Author, id, **kwargs)
        except (NoResultFound, MultipleResultsFound):
            raise
        except EditItem:
            raise EditAuthor
        else:
            return id

    def delete_author(self, id):
        """delete an author
           delete all the author ideas first"""

        if self.get_author(id):
            self.delete_author_ideas(id)
            try:
                self._delete_item(Author, id)
            except DeleteItem:
                raise DeleteAuthor
        else:
                raise InvalidAuthor
        return id

    def delete_author_ideas(self, id):
        """delete all the ideas for an author"""

        if self.get_author(id):
            filters = {'author': self.get_author(id)}
            ideas = self.get_ideas(filters=filters)
            for idea in ideas:
                self.delete_idea(idea.id)

    #
    # Ideas
    #

    def get_idea_count(self):
        """return a count of ideas"""
        return self._get_item_count(Idea)

    def get_idea(self, id):
        """return the requested idea"""
        return self._get_item(Idea, id)

    def get_ideas(self, filters={}, limit=None, order=None):
        """return a list of ideas"""
        return self._get_items(Idea, filters=filters, limit=limit, order=order)

    def add_idea(self, title, idea, author_id):
        """add an idea to the database
           return id of new entry"""

        if title:

            author = self.get_author(author_id)
            filters = {'author': author, 'title': title}
            kwargs = {'title': title, 'idea': idea, 'author': author}

            # check whether the idea already exists
            if len(self._get_items(Idea, filters=filters)) > 0:
                raise DuplicateIdea

            # add the idea
            try:
                new_idea_id = self._add_item(Idea, filters, **kwargs)
            except AddItem:
                raise AddIdea

            return new_idea_id

        else:
            raise AddIdea

    def edit_idea(self, id, **kwargs):
        """edit an idea already in the database"""
        try:
            self._edit_item(Idea, id, **kwargs)
        except (NoResultFound, MultipleResultsFound):
            raise
        except EditItem:
            raise EditIdea
        else:
            return id

    def delete_idea(self, id):
        """delete an idea from the database"""

        try:
            self._delete_item(Idea, id)
        except InvalidItem:
            raise InvalidIdea
        except DeleteItem:
            raise DeleteIdea
        else:
            return id

__all__ = ['Agora', ]
