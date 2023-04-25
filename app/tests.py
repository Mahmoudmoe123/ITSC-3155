import unittest
from app import app, db

class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        with app.app_context():
            self.assertIsNotNone(db.engine.connect())

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_landing(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()