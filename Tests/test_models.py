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

    def test_unique_username(self):

        user1 = User(username="aidan")
        user1.set_password("password")

        user2 = User(username="aidan")
        user2.set_password("password")

        db.session.add(user1)
        db.session.commit()

        db.session.add(user2)

        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
    
    def test_one_user_one_prompt_drawing(self):

        user = User(username="aidan")
        user.set_password("password")

        prompt = Prompt(
            text="Draw a cat",
            date=date.today()
        )

        db.session.add_all([user, prompt])
        db.session.commit()

        drawing1 = Drawing(
            image="img1",
            user_id=user.id,
            prompt_id=prompt.id
        )

        drawing2 = Drawing(
            image="img2",
            user_id=user.id,
            prompt_id=prompt.id
        )

        db.session.add(drawing1)
        db.session.commit()

        db.session.add(drawing2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

        db.session.rollback()

    def test_user_saved_to_database(self):

        user = User(username="aidan")
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        found = User.query.filter_by(username="aidan").first()

        self.assertIsNotNone(found)
        self.assertTrue(found.check_password("password"))

    def test_unique_vote_constraint(self):

        # Create user
        user = User(username="aidan")
        user.set_password("password")

        # Create prompt
        prompt = Prompt(
            text="Draw a cat",
            date=date.today()
        )

        db.session.add_all([user, prompt])
        db.session.commit()

        # Create drawing
        drawing = Drawing(
            image="img1",
            user_id=user.id,
            prompt_id=prompt.id
        )

        db.session.add(drawing)
        db.session.commit()

        # First vote (valid)
        vote1 = Vote(
            voter_id=user.id,
            drawing_id=drawing.id
        )

        db.session.add(vote1)
        db.session.commit()

        # Second vote (same user + same drawing → should fail)
        vote2 = Vote(
            voter_id=user.id,
            drawing_id=drawing.id
        )

        db.session.add(vote2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

        db.session.rollback()