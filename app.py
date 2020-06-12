import os
from flask import Flask, render_template, redirect, session, flash, request, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Favorite, List
from habitable_zone import HabitableZoneCheck
from process_search import ProcessSearch
from forms import SearchForm, SignUpForm, LoginForm, CreateListForm
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///exoplanets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

connect_db(app)

db.create_all()

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.before_request
def add_user_to_g():
    """Add logged in user to global"""

    if "USERNAME" in session:
        g.user = User.query.filter_by(username=session["USERNAME"]).first()

    else:
        g.user = None

@app.route("/")
def get_home_page():
    """Redirects to signup or user detail page"""

    if g.user:
        return redirect(f"/users/{g.user.username}")
    
    return redirect("/signup")  

@app.route("/signup", methods=["GET", "POST"])
def get_signup_page():
    """Renders signup form and redirects to user details"""

    if g.user:
        return redirect(f"/users/{g.user.username}")

    form = SignUpForm()

    if form.validate_on_submit():
        user = User.signup(
                           username=form.username.data,
                           password=form.password.data,
                           email=form.email.data,
                           first_name=form.first_name.data,
                           last_name=form.last_name.data
                           ) 

        db.session.commit()
        session["USERNAME"] = user.username

        return redirect(f"/users/{user.username}")

    return render_template("signup.html", form=form)

@app.route("/users/<username>")
def show_user_details(username):
    """Renders user details page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")
    
    user = User.query.filter_by(username=username).first()

    return render_template("user.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def show_login():
    """Renders login page and processes login form"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
                           username=form.username.data,
                           password=form.password.data,
                           ) 

        if user:
            session["USERNAME"] = user.username

            return redirect(f"/users/{user.username}")

        else: 
            flash("Invalid username or password.")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs out user and clears session"""

    if "USERNAME" in session:
        del session["USERNAME"]
    else:
        flash("You must be logged in.")    

    return redirect("/")

@app.route("/users")
def direct_users():
    """Redirects to user details page or signup page"""

    return redirect("/") 

@app.route("/users/<username>/lists")   
def direct_lists():
    """Redirects to user details page or signup page"""

    return redirect("/")

@app.route("/users/<username>/lists/create", methods=["GET", "POST"])  
def show_create_list(username):
    """Displays create list form and processes form submission"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    form = CreateListForm()

    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        new_list = List(
                        name=form.name.data,
                        description=form.description.data,
                        user_id=user.id
                        ) 
        db.session.add(new_list)
        db.session.commit()

        return redirect(f"/users/{user.username}")

    return render_template("create_list.html", form=form)

@app.route("/users/<username>/lists/<int:list_id>")
def show_list(username, list_id):
    """Renders list details page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user_list = List.query.get(list_id)

    return render_template("list.html", user_list=user_list)  

@app.route("/users/<username>/lists/<int:list_id>/add", methods=["POST"]) 
def add_planet(username, list_id):
    """Adds a planet to a user list and redirects to search results page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user_list = List.query.get(list_id)
    user = user_list.user

    planet_name = request.json["planet"]
    favorite = Favorite(planet_name=planet_name, list_id=user_list.id)

    response = {
                 "new_favorite": {
                   "list" : user_list.name,
                   "planet": planet_name
                 }
               }

    return (jsonify(response), 201)           

@app.route("/planets/<planet_name>")
def get_details(planet_name):
    
    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    resp = requests.get("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" +
                         "table=exoplanets&select=pl_name,pl_orbsmax,pl_rade, pl_masse,pl_hostname," +
                         "st_optmag,st_dist,st_spstr,st_mass,st_rad,st_teff,st_bmvj&" +
                         f"where=pl_name like '{planet_name}%25'&format=json")
    # search =  ProcessSearch({'pl_name': "planet_name"})
    # resp = requests.get(search.create_api_query())


    planet = resp.json()[0]
    check_zone = HabitableZoneCheck(
                                    planet['st_optmag'], 
                                    planet['st_dist'], 
                                    planet['st_spstr'],
                                    planet['pl_orbsmax']
                                    )
   
    return render_template("planet.html", planet=planet, habitable=check_zone.in_habitable_zone()) 

@app.route("/planets/search/form")
def show_search():
    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    return render_template("search.html")

@app.route("/planets/search", methods=["GET","POST"])
def search_planets():
    """Renders search form page and processes form"""

    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    if request.form:
        resp = request.form
        parameters = {}
        if resp.get("all", None):
            parameters["all"] = "on"
        elif resp.get('pl_name', None):
            parameters["pl_name"] = resp["pl_name"]
        elif resp.get('pl_hostname', None):
            parameters["pl_hostname"] = resp["pl_hostname"] 
        else:
            for key,value in request.form.items():
                parameters[key] = value
        
        session["PARAMETERS"] = parameters
    
        if resp.get('habitable', None):
            return redirect("/planets/habitable")

        return redirect("/planets/results")      
        
    return render_template("search.html")

@app.route("/planets/results")
def get_search_results():
    """Render search results"""

    parameters = session["PARAMETERS"]
    del session["PARAMETERS"]
    search = ProcessSearch(parameters)
    print(search.create_api_query())

    session["SEARCH"] = search.create_api_query()
    resp = requests.get(search.create_api_query())

    return render_template("results.html", planets = resp.json(), parameters=parameters)

@app.route("/planets/habitable")
def get_habitable_results():
    """Searches for and returns planets in habitable zone"""

    planets = []
    parameters = {}
    search = ""

    if session.get("PARAMETERS", None):
        parameters = session["PARAMETERS"]
        del session["PARAMETERS"]
    else:
        parameters = {"all": "on"}    
    
    search = ProcessSearch(parameters)        
    session["SEARCH"] = search.create_api_query()
    resp = requests.get(search.create_api_query())                                 
    
    for planet in resp.json():
        if planet['st_optmag'] and planet['st_dist'] and planet['st_spstr'] and planet['pl_orbsmax']:
            check_zone = HabitableZoneCheck(
                                        planet['st_optmag'], 
                                        planet['st_dist'], 
                                        planet['st_spstr'],
                                        planet['pl_orbsmax']
                                        )

            if check_zone.in_habitable_zone() == True:
                planets.append(planet)                        

    return render_template("results.html", planets=planets, parameters=parameters)