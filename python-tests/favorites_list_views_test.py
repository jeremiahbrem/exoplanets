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

    def test_show_create_list(self):
        """Testing display of create new list form page"""

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
            self.assertIn("Test's page", html)
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
            self.assertIn("Test's page", html)
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
    def test_show_edit_list(self):
        """Testing display of edit list form page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.list)    
            resp = client.get(f"/users/testuser/lists/{self.list.id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit List", html)
            del change_session['USERNAME']

    def test_show_edit_list_not_logged_in(self): 
        """Testing access to edit list when not logged in"""

        with app.test_client() as client:
            resp = client.get(f"/users/testuser/lists/{self.list.id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access.", html)
    
    def test_show_edit_list_unauthorized(self): 
        """Testing access to edit list on another users page"""

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
            user = User.query.filter_by(username="testuser2").first()
            user2_list = List(name="testplanets2", description="my testplanets2", user_id=user.id)
            db.session.add(user2_list)        
            db.session.commit()

            get_list = List.query.filter_by(name="testplanets2").first()

            resp = client.get(f"/users/testuser2/lists/{get_list.id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test's page", html)
            self.assertIn("Unauthorized access.", html)
            del change_session["USERNAME"]

    def test_edit_list_post(self):
        """Testing edit list from form"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser" 

            db.session.add(self.list)      

            data = {"name": "testplanets2", "description": "my testplanets 2"}
            resp = client.post(f"/users/testuser/lists/{self.list.id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("GJ 876 c", html)
            self.assertIn("testplanets2", html)
            del change_session["USERNAME"]
    
    def test_edit_list_invalid(self):
        """Testing edit list from invalid inputs"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser" 

            db.session.add(self.list)      

            data = {"name": "", "description": "my testplanets 2"}
            resp = client.post(f"/users/testuser/lists/{self.list.id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit List", html)
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

            resp = client.get(f"/users/testuser/lists/{self.list.id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access.", html)

    def test_show_list_unauthorized(self): 
        """Testing access to list on another users page"""

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
            self.assertIn("Test2's page", html)
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
            self.assertIn('Habitability Zone: <span id="habitable">Habitable</span>', html)
            del change_session["USERNAME"]      

    def test_show_planet_not_logged_in(self):
        """Testing planet detail access if not logged in"""

        with app.test_client() as client:  
            resp = client.get(f"/planets/GJ 876 c", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("You must be logged in.", html)

    def test_add_planet(self):
        """Testing adding a planet to a user's list"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.list)

            data = {"list_id": self.list.id, "planets": ["11 Com b"]}
            resp = client.post(f"/users/testuser/favorites/add", json=data, follow_redirects=True)
            messages = resp.json["messages"]

            self.assertEqual(resp.status_code, 201)
            self.assertIn("11 Com b added to testplanets", messages)
            self.assertEqual(len(self.list.favorites), 2)
            del change_session["USERNAME"]

    def test_add_planets(self):
        """Testing adding multiple planets to a user's list"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.list)

            data = {"list_id": self.list.id, "planets": ["11 Com b", "16 Cyg B b", "GJ 229 A c"]}
            resp = client.post(f"/users/testuser/favorites/add", json=data, follow_redirects=True)
            messages = resp.json["messages"]
        
            self.assertEqual(resp.status_code, 201)
            self.assertIn("11 Com b added to testplanets", messages)
            self.assertIn("16 Cyg B b added to testplanets", messages)
            self.assertIn("GJ 229 A c added to testplanets", messages)
            self.assertEqual(len(self.list.favorites), 4)
            del change_session["USERNAME"]     

    def test_add_planet_unauthorized(self):
        """Testing adding a planet to another user's list"""

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

            data = {"list_id": self.list.id, "planets": ["11 Com b"]}
            resp = client.post(f"/users/testuser/favorites/add", json=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2's page", html)
            self.assertIn("Unauthorized access", html)
            del change_session["USERNAME"]

    def test_add_planet_not_logged_in(self):
        """Testing adding a planet to a user's list while not logged in"""

        with app.test_client() as client:

            db.session.add(self.list)

            data = {"list_id": self.list.id, "planets": ["11 Com b"]}
            resp = client.post(f"/users/testuser/favorites/add", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access", html)  

    def test_delete_favorite(self):
        """Testing deletion of favorite from list"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.list)

            data = {"list_id": self.list.id, "planet": "GJ 876 c"}
            resp = client.post(f"/users/testuser/favorites/delete", json=data, follow_redirects=True)
            message = resp.json
        
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(message, "GJ 876 c deleted from list.")
            self.assertEqual(len(self.list.favorites), 0)
            del change_session["USERNAME"]

    def test_delete_favorite_unauthorized(self):
        """Testing deleting a planet from another user's list"""

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

            data = {"list_id": self.list.id, "planet": "GJ 876 c"}
            resp = client.post(f"/users/testuser/favorites/delete", json=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2's page", html)
            self.assertIn("Unauthorized access", html)
            del change_session["USERNAME"]

    def test_delete_favorite_not_logged_in(self):
        """Testing deleting a planet while not logged in"""

        with app.test_client() as client:

            db.session.add(self.list)

            data = {"list_id": self.list.id, "planets": ["11 Com b"]}
            resp = client.post(f"/users/testuser/favorites/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access", html)        

    def test_delete_list(self):
        """Testing deletion of list"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.list)

            resp = client.post(f"/users/testuser/lists/{self.list.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn("List deleted.", html)
            self.assertIsNone(List.query.get(self.list.id))
            del change_session["USERNAME"]

    def test_delete_list_unauthorized(self):
        """Testing deleting a list from another user"""

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

            data = {"list_id": self.list.id}
            resp = client.post(f"/users/testuser/lists/{self.list.id}/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2's page", html)
            self.assertIn("Unauthorized access", html)
            del change_session["USERNAME"]

    def test_delete_favorite_not_logged_in(self):
        """Testing deleting a planet while not logged in"""

        with app.test_client() as client:

            db.session.add(self.list)

            data = {"list_id": self.list.id}
            resp = client.post(f"/users/testuser/lists/{self.list.id}/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)
            self.assertIn("Unauthorized access", html)

    def test_create_list_axios(self):              
        """Testing creating a list from results page axios request"""   

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            db.session.add(self.user)

            data = {"name": "testlist2"}
            resp = client.post(f"/users/testuser/favorites/create-list", json=data, follow_redirects=True)
            new_list = resp.json

            get_list = List.query.filter_by(name=new_list["list_name"], user_id=self.user.id).first()

            self.assertEqual(resp.status_code, 201)
            self.assertEqual(new_list['list_id'], get_list.id)
            self.assertEqual(new_list['list_name'], "testlist2")
            self.assertEqual(len(self.user.lists), 2)
            del change_session["USERNAME"]     