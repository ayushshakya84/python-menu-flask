import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Linux Menu Authentication', response.data)

    def test_authentication_success(self):
        response = self.app.post('/authenticate', data=dict(password='ayush'))
        self.assertEqual(response.status_code, 302)  # Redirect to menu
        self.assertIn(b'/menu', response.headers['Location'])

    def test_authentication_failure(self):
        response = self.app.post('/authenticate', data=dict(password='wrongpassword'))
        self.assertEqual(response.status_code, 302)  # Redirect to index
        self.assertIn(b'/', response.headers['Location'])

    def test_menu_access(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.get('/menu')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Linux Menu', response.data)

    def test_create_file(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/local_create_file', data=dict(file_name='testfile.txt'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'touch testfile.txt', response.data)

    def test_create_folder(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/local_create_folder', data=dict(folder_name='testfolder'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'mkdir testfolder', response.data)

    def test_show_date(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/show_date')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'date', response.data)

    def test_show_calendar(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/show_calendar')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'cal', response.data)

    def test_install_software(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/install_software', data=dict(software_name='nano'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'yum install -y nano', response.data)

    def test_show_ip(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/show_ip')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'ifconfig', response.data)

    def test_ssh_execute(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/ssh_execute', data=dict(remote_ip='127.0.0.1', remote_user='user', remote_command='ls'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'ssh user@127.0.0.1 ls', response.data)

    def test_execute_custom_command(self):
        self.app.post('/authenticate', data=dict(password='ayush'))
        response = self.app.post('/execute', data=dict(command='ls'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'ls', response.data)

if __name__ == '__main__':
    unittest.main()
