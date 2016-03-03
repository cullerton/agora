import unittest

from logging import getLogger
logger = getLogger(__name__)


def _populate_test_db(session):
    from agora.models import Author, Idea

    # add 2 authors
    [session.add(Author(
        'user_%s' % author,
        'User %s' % author,
        'user_%s@example.com' % author))
        for author in range(1, 3)]

    # add 3 ideas for each of the authors
    [[session.add(Idea(
        'Idea %s' % idea,
        'This is idea number %s' % idea,
        session.query(Author).filter_by(id=author_id).one()))
        for idea in range(1, 4)]
        for author_id in range(1, session.query(Author).count() + 1)]


def _initialize_test_db():

    from agora.models import Base

    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    DBSession = scoped_session(sessionmaker())
    DBSession.configure(bind=engine)

    _populate_test_db(DBSession)

    return DBSession


class AgoraBase(unittest.TestCase):

    def setUp(self):
        self.session = _initialize_test_db()

    def tearDown(self):
        self.session.remove()

    def _Agora(self):
        from agora import Agora
        return Agora(self.session)


class AgoraAuthorTests(AgoraBase):

    def test_get_author_count(self):
        """should return a scalar
           equal to the number of records added in _initialize_test_db"""
        agora = self._Agora()
        self.assertEqual(agora.get_author_count(), 2)

    def test_get_authors(self):
        """should return a list of length author_count"""
        agora = self._Agora()
        author_count = agora.get_author_count()
        authors = agora.get_authors()

        self.assertIsInstance(authors, list)
        self.assertEqual(len(authors), author_count)

    def test_get_authors_with_limit(self):
        """should return a list of length limit"""
        agora = self._Agora()
        author_count = agora.get_author_count()

        for limit in (0, 1, author_count):

            authors = agora.get_authors(limit=limit)
            self.assertIsInstance(authors, list)
            self.assertEqual(len(authors), limit)

    def test_get_authors_bad_limit(self):
        """should return a list of length author_count"""
        agora = self._Agora()
        author_count = agora.get_author_count()

        for limit in (-1, author_count + 1):
            authors = agora.get_authors(limit=limit)
            self.assertIsInstance(authors, list)
            self.assertEqual(len(authors), author_count)

    def test_get_author(self):
        """should return an author"""
        agora = self._Agora()
        from agora.models import Author
        for id in range(1, agora.get_author_count()):
            self.assertIsInstance(agora.get_author(id), Author)

    def test_get_bad_author(self):
        """should return None"""
        agora = self._Agora()
        author_count = agora.get_author_count()
        for i in (-1, 0, author_count + 1):
            self.assertIsNone(agora.get_author(i))

    def test_get_author_repr(self):
        agora = self._Agora()
        for id in range(1, agora.get_author_count()):
            self.assertIn("User %s" % id, agora.get_author(id).__repr__())

    def test_add_author(self):
        agora = self._Agora()

        username = 'test_user'
        fullname = 'Test User'
        email = 'test_user@company.com'
        new_author_id = agora.add_author(username=username,
                                         fullname=fullname,
                                         email=email)

        test_author = agora.get_author(new_author_id)
        self.assertEqual(username, test_author.username)

    def test_edit_author(self):
        agora = self._Agora()
        author_count = agora.get_author_count()

        for id in range(1, author_count):

            username = "edited_user_%s" % id
            fullname = "Edited User %s" % id
            email = "edited_user%s@example.com" % id
            agora.edit_author(id, username=username, fullname=fullname,
                              email=email)
            test_author = agora.get_author(id)
            self.assertEqual(username, test_author.username)
            self.assertEqual(fullname, test_author.fullname)
            self.assertEqual(email, test_author.email)

    def test_edit_bad_author(self):
        agora = self._Agora()
        author_count = agora.get_author_count()
        from sqlalchemy.orm.exc import NoResultFound

        for id in (-1, 0, author_count + 1):
            username = 'bad_user'
            fullname = "Bad User"
            email = 'bad_user@example.com'
            with self.assertRaises(NoResultFound):
                agora.edit_author(
                    id,
                    username=username,
                    fullname=fullname,
                    email=email)

    def test_delete_author(self):
        agora = self._Agora()
        author_count = agora.get_author_count()

        for id in range(1, author_count):
            self.assertEqual(agora.delete_author(id), id)

    def test_delete_bad_author(self):
        agora = self._Agora()
        author_count = agora.get_author_count()
        from agora.exceptions import InvalidAuthor

        for id in (-1, 0, author_count + 1):
            with self.assertRaises(InvalidAuthor):
                agora.delete_author(id)


class AgoraIdeaTests(AgoraBase):

    def test_get_idea_count(self):
        """should return a scalar
           equal to the number of records added in _initialize_test_db"""
        agora = self._Agora()
        # we should know how the idea count
        self.assertEqual(agora.get_idea_count(), 6)

    def test_get_ideas(self):
        """should return a list of length idea_count"""
        agora = self._Agora()
        idea_count = agora.get_idea_count()
        ideas = agora.get_ideas()

        # we should get a list and know its length
        self.assertIsInstance(ideas, list)
        self.assertEqual(len(ideas), idea_count)

    def test_get_ideas_with_limit(self):
        """should return a list of length limit"""
        agora = self._Agora()
        idea_count = agora.get_idea_count()

        for limit in (0, 1, idea_count):

            ideas = agora.get_ideas(limit=limit)
            self.assertIsInstance(ideas, list)
            self.assertEqual(len(ideas), limit)

    def test_get_ideas_bad_limit(self):
        """should return a list of length idea_count"""
        agora = self._Agora()
        idea_count = agora.get_idea_count()

        for limit in (-1, idea_count + 1):
            ideas = agora.get_ideas(limit=limit)
            self.assertIsInstance(ideas, list)
            self.assertEqual(len(ideas), idea_count)

    def test_get_idea(self):
        """should return an idea"""
        agora = self._Agora()
        from agora.models import Idea
        for id in range(1, agora.get_idea_count()):
            self.assertIsInstance(agora.get_idea(id), Idea)

    def test_get_bad_idea(self):
        """should return None"""
        agora = self._Agora()
        idea_count = agora.get_idea_count()
        for i in (-1, 0, idea_count + 1):
            self.assertIsNone(agora.get_idea(i))

    def test_get_idea_repr(self):
        agora = self._Agora()
        for id in range(1, agora.get_idea_count()):
            self.assertRegexpMatches(
                agora.get_idea(id).__repr__(), 'Idea \d+, User \d+')

    def test_add_idea(self):
        agora = self._Agora()

        title = 'My Test Title'
        idea = 'My test idea'
        author_id = 1
        new_idea_id = agora.add_idea(title=title,
                                     idea=idea,
                                     author_id=author_id)

        test_idea = agora.get_idea(new_idea_id)
        self.assertEqual(title, test_idea.title)
        self.assertEqual(idea, test_idea.idea)

    def test_edit_idea(self):
        agora = self._Agora()
        idea_count = agora.get_idea_count()

        for id in range(1, idea_count):

            agora.edit_idea(id, title='Edited Title',
                            idea='This is the edited idea.')
            test_idea = agora.get_idea(id)
            self.assertEqual('Edited Title', test_idea.title)
            self.assertEqual('This is the edited idea.', test_idea.idea)

    def test_edit_bad_idea(self):
        agora = self._Agora()
        idea_count = agora.get_idea_count()
        from sqlalchemy.orm.exc import NoResultFound

        for id in (-1, 0, idea_count + 1):
            with self.assertRaises(NoResultFound):
                agora.edit_idea(id, title='Bad Edited Title',
                                idea='This is the edited bad idea.')

    def test_delete_idea(self):
        agora = self._Agora()
        idea_count = agora.get_idea_count()

        for id in range(1, idea_count):
            self.assertEqual(agora.delete_idea(id), id)

    def test_delete_bad_idea(self):
        agora = self._Agora()
        idea_count = agora.get_idea_count()
        from agora.exceptions import InvalidIdea

        for id in (-1, 0, idea_count + 1):
            with self.assertRaises(InvalidIdea):
                agora.delete_idea(id)
