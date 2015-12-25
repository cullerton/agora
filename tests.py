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
        idea = Idea(title='First Idea!', idea='This is the first idea.')
        DBSession.add(idea)
        idea = Idea(title='YA Idea!', idea='This is YA idea.')
        DBSession.add(idea)
        idea = Idea(title='Third Idea!', idea='This is the third idea.')
        DBSession.add(idea)
        idea = Idea(title='My Idea!', idea='This is my idea.')
        DBSession.add(idea)
        idea = Idea(title='Fifth Idea!', idea='This is the fifth idea.')
        DBSession.add(idea)
        idea = Idea(title='An Idea!', idea='This is an idea.')
        DBSession.add(idea)
        author = Author('some_user', 'Full Name', 'username@company.com')
        DBSession.add(author)
    return DBSession


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
        from agora.agora import InvalidIdea

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
        result = agora.delete_author(id)
        self.assertIs(InvalidIdea, result)

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
        agora = self._Agora()

        idea = agora.get_idea(0)
        from agora.agora import InvalidIdea
        self.assertIs(idea, InvalidIdea)

        idea = agora.get_idea(7)
        self.assertIs(idea, InvalidIdea)

        idea = agora.get_idea(1)
        from agora import Idea
        self.assertIsInstance(idea, Idea)

    def test_add_idea(self):
        agora = self._Agora()

        title = 'My Test Title'
        idea = 'My test idea'
        new_idea_id = agora.add_idea(title=title, idea=idea)

        logger.info("test_add_idea: new_idea_id: %s " % new_idea_id)
        test_idea = agora.get_idea(new_idea_id)
        self.assertIn(title, test_idea.title)

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


# class AgoraAPITests(unittest.TestCase):
#     def setUp(self):
#         self.session = _initTestingDB()
#         self.config = testing.setUp()

#     def tearDown(self):
#         testing.tearDown()
#         # from .models import DBSession
#         # DBSession.remove()
#         self.session.remove()

#     def _callAgoraAPI(self, request):
#         from agora.api import AgoraAPI
#         return AgoraAPI(request)

#     def test_get_ideas(self):

#         request = testing.DummyRequest()
#         api = self._callAgoraAPI(request)
#         # idea_count = api.get_idea_count()

#         response = api.get_ideas()

#         self.assertIsInstance(response, list)
#         self.assertEqual(len(response), 5)
#         self.assertIn('First Idea', response[0]['title'])
#         self.assertIn('YA Idea', response[1]['title'])

#     def test_get_idea(self):
#         from pyramid.response import Response

#         request = testing.DummyRequest()
#         request.matchdict['idea'] = 1
#         api = self._callAgoraAPI(request)
#         idea = api.get_idea()

#         self.assertIsInstance(idea, Response)
#         self.assertIn(b'First Idea', idea.body)

#     def test_add_idea(self):
#         request = testing.DummyRequest(post={'title': 'My test title',
#                                              'idea': 'My test idea'})
#         api = self._callAgoraAPI(request)
#         response = api.add_idea()

#         self.assertEqual('201 Created', response.status)

#     # def test_edit_idea(self):
#     #     request = testing.DummyRequest(put={'title': 'My edited title',
#     #                                         'idea': 'My edited idea'})
#     #     api = self._callAgoraAPI(request)
#     #     response = api.edit_idea()

#     #     self.assertEqual('201 Created', response.status)

#     def test_delete_idea(self):
#         pass

# #     def test_view_idea_no_idea(self):
# #         request = testing.DummyRequest()
# #         api = self._callAgoraAPI(request)
# #         response = api.view_idea()

# #         self.assertEqual('400 Bad Request', response.status)


class AgoraAPIWebTests(unittest.TestCase):

    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('development.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from agora import DBSession
        DBSession.remove()

    def test_get_ideas(self):

        resp = self.testapp.get('/ideas')
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        self.assertIn(b'Idea', resp.body)

        resp = self.testapp.get('/ideas?limit=1')
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        self.assertIn(b'Idea', resp.body)

    # def test_add_idea(self):
    #     request = testing.DummyRequest(post={'title': 'My test title',
    #                                          'idea': 'My test idea'})
    #     api = self._callAgoraAPI(request)
    #     response = api.add_idea()

    #     self.assertEqual('201 Created', response.status)
