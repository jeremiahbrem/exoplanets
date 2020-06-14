from unittest import TestCase
from flask import session
from models import db, User, List, Favorite
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///exoplanets_test"
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
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
                    email="test@example.com", 
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

    def test_home_page(self):
        """testing home page redirect to signup page"""

        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)               

    def test_signup_page(self):
        """testing home page rendering"""

        with app.test_client() as client:
            resp = client.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)

    def test_signup_page_logged_in(self):
        """Testing if logged-in user redirected to user details page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"
            resp = client.get("/signup", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser", html)
            self.assertIn("testplanets", html)
            del session["USERNAME"]


    def test_signup_page_post(self):
        """testing signup and redirect to user details page""" 

        with app.test_client() as client:
            data = {
                "username": "testuser2", 
                "password": "testpassword", 
                "email": "test2@test.com",
                "first_name": "Jerry", 
                "last_name": "Bremy"
                }
            resp = client.post("/signup", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser2's page", html)

    def test_signup_duplicate_username(self):
        """Testing invalid signup, duplicate username"""

        with app.test_client() as client:
            data = {"username": "testuser", "password": "testpwd", "email": "test2@test.com",
                    "first_name": "Jerry", "last_name": "Bremy"}

            resp = client.post("/signup", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username already exists.", html)
            self.assertIn("Welcome to the Exoplanet App", html)
    
    def test_signup_duplicate_email(self):
        """Testing invalid signup, duplicate email"""

        with app.test_client() as client:
            data = {"username": "testuser2", "password": "testpwd", "email": "test@test.com",
                    "first_name": "Jerry", "last_name": "Bremy"}

            resp = client.post("/signup", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Email already exists.", html)
            self.assertIn("Welcome to the Exoplanet App", html)
    
    def test_signup_empty_input(self):
        """Testing invalid signup, empty input"""

        with app.test_client() as client:
            data = {"username": "", "password": "testpwd", "email": "test2@test.com",
                    "first_name": "Jerry", "last_name": "Bremy"}

            resp = client.post("/signup", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)

    def test_show_login(self):
        """Testing login page rendering"""

        with app.test_client() as client:
            resp = client.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login to your account", html)

    def test_login(self):
        """Testing user login"""
        
        with app.test_client() as client:
            data = {"username": "testuser", "password": "testpassword"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser's page", html)

    def test_invalid_password(self):
        """Testing invalid password login"""

        with app.test_client() as client:
            data = {"username": "testuser", "password": "testpassword2"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login to your account", html)
    
    def test_invalid_username(self):
        """Testing invalid password login"""

        with app.test_client() as client:
            data = {"username": "testuser5", "password": "testpassword"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login to your account", html)

    def test_logout(self):
        """Testing logout and redirect to signup/signin page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"
            resp = client.get("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("testuser", html)
            self.assertIn("Welcome to the Exoplanet App", html)
            del change_session["USERNAME"]

    def test_unauthorized_logout(self):
        """Testing logout if already logged out"""

        with app.test_client() as client:
            resp = client.get("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("You must be logged in.", html)

    def test_show_user(self):
        """Testing rendering of user details page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"
            resp = client.get("/users/testuser", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser's page", html)
            self.assertIn("testplanets", html)
            del change_session["USERNAME"]

    def test_show_user_not_logged_in(self):
        """Testing user page attempt when not logged in"""

        with app.test_client() as client:
            resp = client.get("/users/testuser", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access", html)

    def test_show_user_unauthorized(self):
        """Testing unauthorized access of another user's page"""

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
        
            resp = client.get("/users/testuser2", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser's page", html)
            self.assertIn("testplanets", html)
            self.assertIn("Unauthorized access", html)
            del change_session["USERNAME"]
        
        


         