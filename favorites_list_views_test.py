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

class FavoriteListViewsTestCase(TestCase):
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

    def test_show_create_list(self):
        """Testing home page redirect to signup page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"
            resp = client.get("/users/testuser/lists/create", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create New Planet List", html)
            del change_session['USERNAME']

    def test_show_create_list_not_logged_in(self): 
        """Testing access to create new list when not logged in"""

        with app.test_client() as client:
            resp = client.get("/users/testuser/lists/create", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access.", html)
    
    def test_show_create_list_unauthorized(self): 
        """Testing access to create new list on another users page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            user2 = User.signup(
                    username="testuser2", 
                    first_name="Test2", 
                    last_name="User2", 
                    email="test2@test.com", 
                    password="testpassword2"
                    )

            db.session.commit()

            resp = client.get("/users/testuser2/lists/create", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser's page", html)
            self.assertIn("Unauthorized access.", html)
            del change_session["USERNAME"]

    def test_create_list_post(self):
        """Testing create new list from form"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"   

            data = {"name": "testplanets2", "description": "my testplanets 2"}
            resp = client.post("/users/testuser/lists/create", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser's page", html)
            self.assertIn("testplanets2", html)
            del change_session["USERNAME"]
    
    def test_create_list_invalid(self):
        """Testing create new list from invalid inputs"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"   

            data = {"name": "", "description": "my testplanets 2"}
            resp = client.post("/users/testuser/lists/create", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create New Planet List", html)
            del change_session["USERNAME"]

    def test_show_list(self):
        """Testing rendering of list details page""" 

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"  
            db.session.add(self.list) 

            resp = client.get(f"/users/testuser/lists/{self.list.id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testplanets", html)
            self.assertIn("my testplanets", html)
            del change_session["USERNAME"]

    def test_show_list_not_logged_in(self):
        """Testing show list if not logged in"""  

        with app.test_client() as client:
            user2 = User.signup(
                    username="testuser2", 
                    first_name="Test2", 
                    last_name="User2", 
                    email="test2@test.com", 
                    password="testpassword2"
                    )

            db.session.commit()

            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser2"

            db.session.add(self.list)    

            resp = client.get(f"/users/testuser/lists/{self.list.id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser2's page", html)
            self.assertIn("Unauthorized access.", html)
            del change_session["USERNAME"]

    def test_show_planet(self):
        """Testing rendering of planet details page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"  

            resp = client.get(f"/planets/GJ 876 c", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("GJ 876 c", html)
            self.assertIn("Host Star: GJ 876", html)
            del change_session["USERNAME"]

    def test_show_planet_not_logged_in(self):
        """Testing planet detail access if not logged in"""

        with app.test_client() as client:  
            resp = client.get(f"/planets/GJ 876 c", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("You must be logged in.", html)

    # def test_add_planet(self):
    #     """Testing adding a planet to a user's list"""

    #     with app.test_client() as client:  
    #         data = {"pl_name": "11 Com b"}
    #         resp = client.post(f"/users/{self.user.username}/lists/{self.list.id}/add", data=data, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("testplanets", html)
    #         self.assertIn("11 Com b ", html)   