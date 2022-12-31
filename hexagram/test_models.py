from unittest import TestCase
from app.models import User
from app import bcrypt

class TestUser(TestCase):
    """
    Tests performed to the User object
    """
    def test_password_hash(self):
        """
        Tests hashing password entered by user when registering
        """
        password = '12345678'
        User.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        print("Entered Password: " + password)
        print("Hashed Password: " + User.password_hash)

        self.assertNotEqual(password, User.password_hash)
