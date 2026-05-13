import unittest
from datetime import date

from app import create_app, db
from sqlalchemy.exc import IntegrityError
from config import TestConfig
from app.models import User, Prompt, Drawing, Vote


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class UserModelTests(BaseTestCase):

    def test_password_hashing(self):
        user = User(username="aidan")
        user.set_password("mypassword")

        self.assertNotEqual(user.password_hashed, "mypassword")
        self.assertTrue(user.check_password("mypassword"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_password_is_hashed(self):
        user = User(username="testuser")
        user.set_password("secret123")

        self.assertNotEqual(user.password_hashed, "secret123")

    def test_user_repr(self):
        user = User(id=1, username="aidan")

        self.assertIn("aidan", repr(user))
        self.assertIn("1", repr(user))

    def test_user_email_can_be_none(self):
        user = User(username="testuser")
        user.set_password("password")

        self.assertIsNone(user.email)

    def test_drawing_repr_contains_id(self):
        drawing = Drawing(id=10, user_id=1, prompt_id=2, image="img")

        self.assertIn("10", repr(drawing))