import unittest
import main
from main import app
from flask import Flask

app1 = Flask(__name__)

class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dummy_data = {"username": "jai123", "password": "1234", "last_name": "jagani", "first_name": "jai"}
        self.app = app.test_client()

    def test_user_exists_positive(self):
        self.assertTrue(main.add(self.dummy_data))
        self.assertTrue(main.user_exists(self.dummy_data))

    def test_user_exists_negative(self):
        self.dummy_data["username"] = "jai1234"
        self.assertFalse(main.user_exists(self.dummy_data))


    def test_user_login_positive(self):
        self.assertTrue(main.add(self.dummy_data))
        result = main.login_user(self.dummy_data)
        self.assertEqual(result[1], 200)

    def test_user_login_negative(self):
        self.dummy_data["username"] = "jai12345"
        result = main.login_user(self.dummy_data)
        self.assertEqual(result[1], 400)


    def test_register_user_positive(self):
        self.dummy_data["username"] = "jai123456"
        result = main.register_user(self.dummy_data)
        self.assertEqual(result[1], 200)

    def test_register_user_negative(self):
        self.assertTrue(main.add(self.dummy_data))
        result = main.register_user(self.dummy_data)
        self.assertEqual(result[1], 400)


#functional/integration test cases
    
    def integration_test_registering_user_negative(self):
        payload = """
        {"username": "jai1234", "password": "1234", "last_name": "jagani", "first_name": "jai"}
        """
        result = self.app.post("/api/user", data=payload)
        self.assertEqual(result.status_code, 400)

    def integration_test_registering_user_positive(self):
        payload = """
        {"username": "jai12", "password": "1234", "last_name": "jagani", "first_name": "jai"}
        """
        result = self.app.post("/api/user", data=payload)
        self.assertEqual(result.status_code, 200)

    def integration_test_login_user_negative(self):
        payload = """
        {"username": "jai12", "password": "1234", "last_name": "jagani", "first_name": "jai"}
        """
        result = self.app.post("/api/user", data=payload)
        self.assertEqual(result.status_code, 400)

    def integration_test_login_user_positive(self):
        payload = """
        {"username": "jai1234", "password": "1234", "last_name": "jagani", "first_name": "jai"}
        """
        result = self.app.post("/api/user", data=payload)
        self.assertEqual(result.status_code, 200)
