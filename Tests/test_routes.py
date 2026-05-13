import unittest
from app import create_app

class RouteTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # ---- ROUTE TESTS ----

    def test_index_requires_login(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
   
    def test_browse_requires_login(self):
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 302)

    def test_leaderboard_requires_login(self):
        response = self.client.get('/leaderboard')
        self.assertEqual(response.status_code, 302)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_drawing_requires_login(self):
        response = self.client.get('/drawing')
        self.assertEqual(response.status_code, 302)

    def test_index_contains_content(self):
        response = self.client.get('/')
        self.assertIn(b"<html", response.data)  # basic sanity check

if __name__ == "__main__":
    unittest.main()