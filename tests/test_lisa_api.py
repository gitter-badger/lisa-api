from lisa_api import app, db
from flask import current_app
import unittest


class LisaApiTestCase(unittest.TestCase):
    """Main test cases for LISA-API."""

    def setUp(self):
        """Pre-test activities."""
        app.testing = True
        with app.app_context():
            db.init_app(current_app)
            self.app = app.test_client()

    def test_get_login_test(self):
        """Does hitting the /login endpoint return the proper HTTP code?"""
        response = self.app.get('/login')
        assert response.status_code == 200