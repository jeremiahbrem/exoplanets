from flask import Flask, render_template, redirect, session, flash, request, g
from models import db, connect_db, User, Favorite, List
from habitable_zone import HabitableZoneCheck
from forms import SearchForm, SignUpForm, LoginForm
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///exoplanets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "s8t64h5gs3h1sdf35h4s"

connect_db(app)

db.drop_all()
db.create_all()

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

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs out user and clears session"""

    if "USERNAME" in session:
        del session["USERNAME"]

    return redirect("/")    

@app.route("/habitable")
def get_habitable():
    planets = []
    resp = requests.get(f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" +
                         "table=exoplanets&select=pl_name,pl_orbsmax,st_optmag,st_dist,st_spstr" +
                         "&order=pl_name&format=json")
    
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

    return render_template("habitable.html", planets=planets)

@app.route("/details/<planet_name>")
def get_details(planet_name):
    print(planet_name)
    resp = requests.get("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" +
                         "table=exoplanets&select=pl_name,pl_orbsmax,pl_rade, pl_masse,pl_hostname," +
                         "st_optmag,st_dist,st_spstr,st_mass,st_rad,st_teff,st_bmvj&" +
                         f"where=pl_name like '{planet_name}%25'&format=json")
   
    return render_template("page.html", planet=resp.json()[0])

@app.route("/search")
def search_planets():
    form = SearchForm()

    return render_template("form.html", form=form)                   
        
        