from app import create_app
import unittest

app = create_app()

class FlaskTestRoutes(unittest.TestCase):
    """
    Tests performed to the app Routes
    """
    def test_home_page(self):
        """
        Checks if home page route exists
        """
        with app.test_client() as test:
            response = test.get('/home', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """
        Checks if about page route exists
        """
        with app.test_client() as test:
            response = test.get('/about', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Tests route for registering a new user
        """
        with app.test_client() as test:
            response = test.post('/register', data=dict(username="test",
                                                        email="test@test.com",
                                                        department="security",
                                                        password="Test1234"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        Tests route for login admin
        """
        with app.test_client() as test:
            response = test.get('/login', data=dict(username="dinoqueen",
                                                    password="12345678"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_update_account(self):
        """
        Tests updating dummy admin data
        """
        with app.test_client() as test:
            self.test_login()
            response = test.post('/admin/update_account', data=dict(username="testUpdated",
                                                              email="test@updated.com"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Tests logout dummy user
        """
        with app.test_client() as test:
            self.test_login()
            response = test.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_account(self):
        """
        Tests deleting admin
        """
        with app.test_client() as test:
            self.test_login()
            response = test.post('/admin/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_read_projects(self):
        """
        Test route to see projects
        """
        with app.test_client() as test:
            response = test.post('/admin/projects', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_create_projects(self):
        """
        Test route to create projects
        """
        with app.test_client() as test:
            response = test.post('/admin/add_project', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_update_projects(self):
        """
        Test route to update projects
        """
        with app.test_client() as test:
            response = test.post('/admin/update_project', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_projects(self):
        """
        Test route to delete projects
        """
        with app.test_client() as test:
            response = test.post('/admin/delete_project', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_read_designers(self):
        """
        Test route to see designers
        """
        with app.test_client() as test:
            response = test.post('/admin/designers', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_read_roles(self):
        """
        Test route to see roles
        """
        with app.test_client() as test:
            response = test.post('/admin/roles', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_non_route(self):
        """
        Tests a error routes
        """
        with app.test_client() as test:
            response = test.get('/other_route', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()