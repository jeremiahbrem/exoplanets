import os
from unittest import TestCase
from flask import session
from models import db, User, List, Favorite

os.environ['DATABASE_URL'] = "postgresql:///exoplanet-test"

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class SearchViewsTestCase(TestCase):
    """Testing User view functions"""

    def setUp(self):
        """add sample User, List, and Favorite data."""

        User.query.delete()
        List.query.delete()
        Favorite.query.delete()          

        user = User.signup(
                    username="testuser", 
                    first_name="Test", 
                    last_name="User", 
                    email="test@test.com", 
                    password="testpassword"
                    )

        self.user = User.query.filter_by(username="testuser").first()
        user_list = List(name="testplanets", description="my testplanets", user_id=self.user.id)
        db.session.add(user_list)
        self.list = List.query.filter_by(name="testplanets").first()

        favorite = Favorite(list_id=self.list.id, planet_name="GJ 876 c")
        db.session.add(favorite)
        self.favorite = Favorite.query.filter_by(list_id=self.list.id).first()

        db.session.commit() 

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_search_form(self):
        """Testing rendering of search form page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"
            
            resp = client.get("planets/search", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search Exoplanets", html)
            del change_session['USERNAME']

    def test_search_results_all(self):
        """Testing search results for all exoplanets"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"parameter": "all"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 4164", html)
            del change_session['USERNAME']