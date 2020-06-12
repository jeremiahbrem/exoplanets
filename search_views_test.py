import os
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
            
            resp = client.get("planets/search/form", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search Exoplanets", html)
            del change_session['USERNAME']

    def test_show_search_form_unauthorized(self):
        """Testing show search page while not logged in"""

        with app.test_client() as client:
            resp = client.get("/planets/search/form", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet App", html)      
            self.assertIn("You must be logged in.", html)     

    def test_search_results_all(self):
        """Testing search results for all exoplanets"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"all": "on"}
            resp = client.post("/planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 4164", html)
            self.assertIn("KOI-351 h", html)
            del change_session['USERNAME']
    
    def test_search_results_st_mass(self):
        """Testing search results solar mass between 0.5 and 1"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_mass": "on", "st_mass_min": 0.5, "st_mass_max": 1.0}
            resp = client.post("/planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 1589", html)
            self.assertIn("Kepler-94 b", html)
            self.assertIn("0.81", html)
            del change_session['USERNAME']
    
    def test_search_results_st_rad(self):
        """Testing search results with solar radius between 0.5 and 1"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_rad": "on", "st_rad_min": 0.5, "st_rad_max": 1.0}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 1786", html)
            self.assertIn("Kepler-93 b", html)
            del change_session['USERNAME']

    def test_search_results_st_opt_mag(self):
        """Testing search results with solar optical magnitude < 3"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_optmag": "on", "st_optmag_max": 3.0}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 5", html)
            self.assertIn("HD 62509 b", html)
            del change_session['USERNAME']

    def test_search_results_st_bmvj(self):
        """Testing search results with star color index > 3"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_bmvj": "on", "st_bmvj_min": 3}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 2", html)
            self.assertIn("HIP 79431 b", html)
            del change_session['USERNAME']

    def test_search_results_st_teff(self):
        """Testing search results solar surface temp > 10,000K"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_teff": "on", "st_teff_min": 10000}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 14", html)
            self.assertIn("kap And b", html)
            del change_session['USERNAME']

    def test_search_results_st_spstr(self):
        """Testing search results solar spectral-type of M5"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_spstr": "on", "st_spstr_type": "M5"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 6", html)
            self.assertIn("Proxima Cen b", html)
            del change_session['USERNAME']

    def test_search_results_st_dist(self):
        """Testing search results solar distance less than 3 parsecs"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_dist": "on", "st_dist_max": 3.0}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 2", html)
            self.assertIn("Proxima Cen b", html)
            del change_session['USERNAME']

    def test_search_results_pl_hostname(self):
        """Testing search results host star name like TRAPPIST"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_hostname": "TRAPPIST"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 7", html)
            self.assertIn("TRAPPIST-1 b", html)
            del change_session['USERNAME']

    def test_search_results_pl_name(self):
        """Testing search results planet name starting with GJ"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_name": "GJ"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 91", html)
            self.assertIn("GJ 163 b", html)
            del change_session['USERNAME']

    def test_search_results_pl_orbsmax(self):
        """Testing search results planet semi-major axis orbit between .99 and 1.1 AU"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_orbsmax": "on", "pl_orbsmax_min": 0.99, "pl_orbsmax_max": 1.1}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 29", html)
            self.assertIn("KOI-351 h", html)
            del change_session['USERNAME']

    def test_search_results_pl_rade(self):
        """Testing search results planet radius over 20 earth radii"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_rade": "on", "pl_rade_min": 20.0}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 2", html)
            self.assertIn("HD 100546 b", html)
            del change_session['USERNAME']

    def test_search_results_pl_pnum(self):
        """Testing search results number of planets in system over 6"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_pnum": "on", "pl_pnum_min": 6.0}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 15", html)
            self.assertIn("KOI-351 h", html)
            del change_session['USERNAME']

    def test_search_results_pl_mass(self):
        """Testing search results planet mass between 0.99 and 1.1"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_masse": "on", "pl_masse_min": 0.99, "pl_masse_max": 1.1}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 1", html)
            self.assertIn("L 98-59 b", html)
            del change_session['USERNAME']

    def test_search_results_habitable(self):
        """Testing search results planets in habitable zone"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"habitable": "on"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 68", html)
            self.assertIn("16 Cyg B b", html)
            del change_session['USERNAME']

    def test_search_results_habitable_st_mass(self):
        """Testing search results habitable zone and star mass"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"habitable": "on", "st_mass": "on", "st_mass_min": 0.5, "st_mass_max": 1}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 14", html)
            self.assertIn("HD 43197 b", html)
            del change_session['USERNAME']       
    
    def test_search_results_st_mass_habitable(self):
        """Testing search results star mass and habitable zone"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_mass": "on", "st_mass_min": 0.5, "st_mass_max": 1, "habitable": "on"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 14", html)
            self.assertIn("HD 43197 b", html)
            del change_session['USERNAME']       
    
    def test_search_results_st_mass_spectral_type(self):
        """Testing search results star mass and spectral type"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_mass": "on", "st_mass_min": 0.1, "st_mass_max": 0.5, "st_spstr": "on", "st_spstr_type": "M5"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 6", html)
            self.assertIn("GJ 1061 d", html)
            del change_session['USERNAME']       
    
    def test_search_results_spectral_type_st_mass(self):
        """Testing search results spectral type and star mass"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"st_spstr": "on", "st_spstr_type": "M5", "st_mass": "on", "st_mass_min": 0.1, "st_mass_max": 0.5}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 6", html)
            self.assertIn("GJ 1061 d", html)
            del change_session['USERNAME']       
    
    def test_search_results_pl_radius_pl_mass_st_teff(self):
        """Testing search results planet mass, radius and star temp"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["USERNAME"] = "testuser"

            data = {"pl_masse": "on", "pl_masse_min": 0.5, "pl_masse_max": 1, "pl_rade": "on",
                    "pl_rade_min": 0.5, "pl_rade_max": 1, "st_teff": "on", "st_teff_min": 5000}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Planet Search Results", html)
            self.assertIn("count: 1", html)
            self.assertIn("KOI-55 c", html)
            self.assertIn("0.655", html)
            self.assertIn("0.867", html)
            del change_session['USERNAME']       

    def test_search_unauthorized(self):
        """Testing search post attempt not logged in"""

        with app.test_client() as client:
            data = {"habitable": "on"}
            resp = client.post("planets/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Exoplanet", html)
            self.assertIn("You must be logged in.", html)



