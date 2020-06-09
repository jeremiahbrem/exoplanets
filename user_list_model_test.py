import os
from unittest import TestCase
from models import db, User, List, Favorite
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///exoplanet-test"

from app import app

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

db.create_all()

class UserListModelsTestCase(TestCase):
    """Testing Star model functions"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        List.query.delete()
        Favorite.query.delete()

        self.client = app.test_client()          

        user = User(
                    username="testuser", 
                    first_name="Test", 
                    last_name="User", 
                    email="test@test.com", 
                    password="password"
                    )
        db.session.add(user)
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

    def test_user__repr__(self):
        """Testing User __repr__ method"""

        self.assertEqual(f"{self.user}", f"<User #{self.user.id}: testuser>")
    
    def test_list__repr__(self):
        """Testing List __repr__ method"""

        self.assertEqual(f"{self.list}", f"<List #{self.list.id}: testplanets>")

    def test_has_list(self):
        """Testing list relationship to user"""

        self.assertIn(self.list, self.user.lists)
        self.assertEqual(self.user, self.list.user)
        self.assertEqual(self.user.id, self.list.user.id)

    def test_has_favorite(self):
        """Testing favorite relationship to list"""

        self.assertEqual(self.favorite.list_id, self.list.id)
        self.assertEqual(len(self.list.favorites), 1)
        self.assertIn(self.favorite, self.list.favorites)

    def test_signup(self):
        """Testing user signup method"""

        user = User.signup(
                        username="jbrem", 
                        email="jb@testing.com", 
                        password="testpwd",
                        first_name="Jeremiah", 
                        last_name="Brem"
                        )

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "jbrem")
        # make sure password is hashed in database
        self.assertNotEqual(user.password, "testpwd")

    def test_invalid_signup(self):
        """Testing invalid user signup"""

        with self.assertRaises(IntegrityError):
            user = User.signup(
                            username=None, 
                            email="jb@test.com", 
                            password="testpwd",
                            first_name="Jeremiah", 
                            last_name="Brem"
                            )   
            db.session.commit()                               
            
        db.session.rollback()

        with self.assertRaises(IntegrityError):
            user = User.signup(
                            username="jbrem", 
                            email=self.user.email, 
                            password="testpwd",
                            first_name="Jeremiah", 
                            last_name="Brem"
                            )  

            db.session.commit()                               
        
        db.session.rollback()

        with self.assertRaises(IntegrityError):
            user = User.signup(
                            username=self.user.username, 
                            email="jb@test.com", 
                            password="testpwd",
                            first_name="Jeremiah", 
                            last_name="Brem"
                            )

            db.session.commit()                               

    def test_authenticate(self):
        """Testing User authenticate method for user login"""

        user = User.signup(
                        username="jbrem", 
                        email="jb@testing.com", 
                        password="testpwd",
                        first_name="Jeremiah", 
                        last_name="Brem"
                        )

        db.session.commit()    
        check_user = User.authenticate(username="jbrem", password="testpwd")

        self.assertIsInstance(check_user, User)

    def test_invalid_authenticate(self):
        """Testing User authenticate method for ivalid login"""

        user = User.signup(
                        username="jbrem", 
                        email="jb@testing.com", 
                        password="testpwd",
                        first_name="Jeremiah", 
                        last_name="Brem"
                        )

        db.session.commit()    
        check_user = User.authenticate(username="jbrem", password="testpd")

        self.assertFalse(check_user)    

