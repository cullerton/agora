import unittest
import transaction
from logging import getLogger
logger = getLogger(__name__)

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from agora import (
        DBSession,
        Idea,
        Author,
        Base
    )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        author = Author('some_user', 'Full Name', 'username@company.com')
        DBSession.add(author)
    with transaction.manager:
        author = DBSession.query(Author).filter_by(username='some_user').one()
        idea = Idea(title='First Idea!',
                    idea='This is the first idea.', author=author)
        DBSession.add(idea)
        idea = Idea(title='YA Idea!',
                    idea='This is YA idea.', author=author)
        DBSession.add(idea)
        idea = Idea(title='Third Idea!',
                    idea='This is the third idea.', author=author)
        DBSession.add(idea)
        idea = Idea(title='My Idea!',
                    idea='This is my idea.', author=author)
        DBSession.add(idea)
        idea = Idea(title='Fifth Idea!',
                    idea='This is the fifth idea.', author=author)
        DBSession.add(idea)
        idea = Idea(title='An Idea!',
                    idea='This is an idea.', author=author)
        DBSession.add(idea)
    return DBSession


# class DBTests(unittest.TestCase):

#     def setUp(self):
#         self.config = testing.setUp()

#     def tearDown(self):
#         testing.tearDown()

#     def test_initialize_db(self):
#         database_uri = "sqlite:///:memory:"

#         from agora import Idea
#         from os import getcwd
#         from os.path import join

#         call_path = join(getcwd(), '..', 'env-35/bin/initialize_agora_db')
#         logger.info("test_initialize_db: call_path: %s" % call_path)

#         from subprocess import call
#         # call_string = "%s/agora/initialize_db.py %s" % (getcwd(), database_uri)
#         # call_string = "%s/../env-35/bin/initialize_agora %s" % (getcwd(), database_uri)
#         # call_string = "%s", "%s" % (call_path, database_uri)
#         session = call([call_path, database_uri])

#         ideas = session.query(Idea)
#         self.assertIs(ideas, list)


class AgoraTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        self.session.remove()

    def _Agora(self):
        from agora.agora import Agora
        return Agora(self.session)

    #
    # Authors
    #

    # def test_get_author_count(self):

    #     agora = self._Agora()
    #     count = agora.get_author_count()

    #     self.assertEqual(count, 1)

    def test_get_authors_no_limit(self):

        agora = self._Agora()
        authors = agora.get_authors()

        self.assertEqual(len(authors), 1)

    def test_get_authors_with_limit(self):
        agora = self._Agora()

        # author_count = agora.get_author_count()

        authors = agora.get_authors(0)
        self.assertEqual(len(authors), 0)

        limit = 2
        authors = agora.get_authors(limit)
        self.assertIsInstance(authors, list)

        limit = -2
        authors = agora.get_authors(limit)
        self.assertEqual(len(authors), 1)

    def test_get_author(self):
        agora = self._Agora()

        from agora import Author
        from agora.agora import InvalidAuthor

        author = agora.get_author(0)
        self.assertIs(author, InvalidAuthor)

        author = agora.get_author(7)
        self.assertIs(author, InvalidAuthor)

        author = agora.get_author(1)
        self.assertIsInstance(author, Author)

    def test_add_author(self):
        agora = self._Agora()
        from agora import Author

        username = 'test_user'
        fullname = 'Test User'
        email = 'test_user@company.com'

        new_author_id = agora.add_author(username=username,
                                         fullname=fullname,
                                         email=email)

        test_author = agora.get_author(new_author_id)
        self.assertIsInstance(test_author, Author)
        # self.assertIn(title, test_author.title)

    def test_edit_author(self):
        agora = self._Agora()

        agora.edit_author(1, username='edited_user', fullname='Edited User',
                          email='edited_user@company.com')
        test_author = agora.get_author(1)
        self.assertEqual('edited_user', test_author.username)
        self.assertEqual('Edited User', test_author.fullname)
        self.assertEqual('edited_user@company.com', test_author.email)

    def test_delete_author(self):
        agora = self._Agora()
        from agora.agora import InvalidAuthor

        # valid id
        id = 1

        # count = agora.get_author_count()
        author = agora.get_author(id)
        logger.info("test_delete_author: author: %s" % author)

        result = agora.delete_author(id)
        logger.info("test_delete_author: result: %s" % result)
        self.assertEqual(result, id)

        # invalid id
        id = 0
        with self.assertRaises(InvalidAuthor):
            agora.delete_author(id)

    #
    # Ideas
    #

    def test_get_ideas_no_limit(self):

        agora = self._Agora()
        ideas = agora.get_ideas()

        self.assertEqual(len(ideas), 5)

    def test_get_ideas_with_limit(self):
        agora = self._Agora()

        ideas = agora.get_ideas(0)
        self.assertEqual(len(ideas), 0)

        limit = 2
        ideas = agora.get_ideas(limit)
        self.assertEqual(len(ideas), limit)

        limit = -2
        ideas = agora.get_ideas(limit)
        self.assertEqual(len(ideas), 5)

    def test_get_idea(self):
        from agora import Idea
        from agora.agora import InvalidIdea

        agora = self._Agora()

        with self.assertRaises(InvalidIdea):
            agora.get_idea(0)

        with self.assertRaises(InvalidIdea):
            agora.get_idea(7)

        idea = agora.get_idea(1)
        self.assertIsInstance(idea, Idea)

    def test_add_idea(self):
        agora = self._Agora()

        new_idea_id = agora.add_idea(title='My Test Title',
                                     idea='My test idea',
                                     author_id=1)

        logger.info("test_add_idea: new_idea_id: %s " % new_idea_id)
        test_idea = agora.get_idea(new_idea_id)
        self.assertIn('My Test Title', test_idea.title)

    def test_edit_idea(self):
        agora = self._Agora()

        agora.edit_idea(1, title='Edited Title',
                        idea='This is the edited first idea.')
        test_idea = agora.get_idea(1)
        self.assertIn('This is the edited first idea', test_idea.idea)

    def test_delete_idea(self):
        agora = self._Agora()

        id = 1

        idea = agora.get_idea(id)
        logger.info("test_delete_idea: idea: %s" % idea)

        result = agora.delete_idea(id)
        logger.info("test_delete_idea: result: %s" % result)
        self.assertEqual(result, id)

        returned = agora.delete_idea(0)
        from agora.agora import InvalidIdea
        self.assertIs(InvalidIdea, returned)
