import unittest
import os
import sys
from xmlrunner import XMLTestRunner
from main import app, db, User

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_login(self):
        response = self.app.post('/register', data=dict(username='testuser', password='testpass', email='test@example.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/login', data=dict(username='testuser', password='testpass'), follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)

    def test_profile_update(self):
        self.app.post('/register', data=dict(username='testuser', password='testpass', email='test@example.com'), follow_redirects=True)
        self.app.post('/login', data=dict(username='testuser', password='testpass'), follow_redirects=True)
        response = self.app.post('/profile', data=dict(email='new@example.com', about='Updated about section'), follow_redirects=True)
        self.assertIn(b'Profile updated successfully!', response.data)

if __name__ == '__main__':
    with open('test-reports/results.xml', 'wb') as output:
        unittest.main(testRunner=XMLTestRunner(output=output))
