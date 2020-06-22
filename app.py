import os, secrets
from flask import Flask, render_template, redirect, session, flash, request, g, jsonify
from flask_mail import Mail, Message
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Favorite, List
from habitable_zone import HabitableZoneCheck
from process_search import ProcessSearch
from forms import SearchForm, SignUpForm, LoginForm, CreateListForm, EditAccountForm, ResetPasswordForm, EnterEmailForm, EditListForm
import requests
from requests import ConnectionError
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL","postgres:///exoplanets")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME', None)
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD', None)
app.config["ADMINS"] = [app.config["MAIL_USERNAME"]]

mail = Mail(app)

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

@app.route("/about")
def show_about():
    """Renders about page"""

    if not g.user:
        return redirect("/")

    return render_template("about.html")    

@app.route("/users/<username>")
def show_user_details(username):
    """Renders user details page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")
    
    user = User.query.filter_by(username=username).first()

    return render_template("user.html", user=user)

@app.route("/users/<username>/edit", methods=["GET", "POST"])
def get_edit_form(username):
    """Renders edit form and redirects to user details"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user = User.query.filter_by(username=username).first()
    form = EditAccountForm(obj=user)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_password = form.new_password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user_check = User.authenticate(
                        username=user.username,
                        password=password,
                        )

        if user_check:
            user.username = username
            if new_password:
                user.password = User.change_password(new_password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name                     

        db.session.commit()
        session["USERNAME"] = user.username
        flash("Account updated.")

        return redirect(f"/users/{user.username}")

    return render_template("edit_account.html", user=user, form=form)    

@app.route("/users/<username>/delete", methods=["GET","POST"])
def delete_user_confirm(username):
    """Renders confirm delete page and processes delete form"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user = User.query.filter_by(username=username).first()

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
                           username=form.username.data,
                           password=form.password.data,
                           ) 

        if user:
            db.session.delete(user)    
            db.session.commit()
            del session["USERNAME"]

        else:
            flash("Invalid username or password")
            return redirect(f"/users/{username}/delete")  

        return redirect("/")

    return render_template("delete_account.html", form=form, user=user)    

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

@app.route("/users/<username>/lists/<int:list_id>/edit", methods=["GET", "POST"])  
def show_edit_list(username, list_id):
    """Displays edit list form and processes form submission"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user_list = List.query.get(list_id)
    user = user_list.user
    
    form = EditListForm(obj=user_list)

    if form.validate_on_submit():
        user_list.name=form.name.data,
        user_list.description=form.description.data,
        
        db.session.commit()

        return redirect(f"/users/{user.username}/lists/{user_list.id}")

    return render_template("edit_list.html", form=form, user_list=user_list)

@app.route("/users/<username>/lists/<int:list_id>")
def show_list(username, list_id):
    """Renders list details page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user_list = List.query.get(list_id)

    return render_template("list.html", user_list=user_list)

@app.route("/users/<username>/lists/<int:list_id>/delete", methods=["POST"])
def delete_list(username, list_id):
    """Deletes user list"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    user_list = List.query.get(list_id)
    db.session.delete(user_list)
    db.session.commit()
    flash("List deleted.")

    return redirect("/")    

@app.route("/users/<username>/favorites/add", methods=["POST"])
@cross_origin()
def add_planet(username):
    """Adds a planet to a user list and redirects to search results page"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    favorites = []
    list_id = request.json["list_id"]
    planets = request.json["planets"]
    user_list = List.query.get(list_id)
    user = user_list.user
 
    for planet in planets:
        if Favorite.query.filter_by(list_id=list_id, planet_name=planet).first() == None:
            favorite = (Favorite(planet_name=planet, list_id=list_id))
            db.session.add(favorite)
            favorites.append(planet)
        else:
            favorites.append(f"You already added {planet} to list.")    
    
    db.session.commit()    

    response = {
                 "new_favorites": {
                   "list" : user_list.name,
                   "planets" : favorites
                 }
               }

    return (jsonify(response), 201)   

@app.route("/users/<username>/favorites/delete", methods=["POST"])
@cross_origin()     
def delete_planet(username):
    """Deletes planet from user list"""

    if not g.user or g.user.username != username:
        flash("Unauthorized access.")
        return redirect("/")

    list_id = request.json["list_id"]
    planet_name = request.json["planet"]
    favorite = Favorite.query.filter_by(list_id=list_id, planet_name=planet_name).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    message = f"{planet_name} deleted from list."  

    return (jsonify(message), 201)
    

@app.route("/planets/<planet_name>")
def get_details(planet_name):
    
    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    search =  ProcessSearch({'pl_name': planet_name})
    resp = requests.get(search.create_api_query())


    planet = resp.json()[0]
    check_zone = HabitableZoneCheck(
                                    planet['st_optmag'], 
                                    planet['st_dist'], 
                                    planet['st_spstr'],
                                    planet['pl_orbsmax']
                                    )
   
    return render_template("planet.html", planet=planet, habitable=check_zone.in_habitable_zone().value) 

@app.route("/planets/search", methods=["GET","POST"])
def search_planets():
    """Renders search form page and processes form"""

    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    if request.form:
        resp = request.form
        parameters = {}
        
        for key,value in request.form.items():
            parameters[key] = value
        
        session["PARAMETERS"] = parameters
    
        if resp.get('habitable', None):
            return redirect("/planets/habitable")

        return redirect("/planets/results/1")      
        
    return render_template("search.html")

@app.route("/planets/results/<int:page>", methods=["GET", "POST"])
def get_search_results(page):
    """Render search results"""

    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    parameters = session["PARAMETERS"]
    
    if request.form:
        resp = request.form['sort']
        parameters["sort_by"] = resp
        session["PARAMETERS"] = parameters
        return redirect("/planets/results/1")

    search = ProcessSearch(parameters)

    session["SEARCH"] = search.create_api_query()
    print(search.create_api_query())
    try:
        resp = requests.get(search.create_api_query())
    except ConnectionError:
        flash("There seems to be a problem accessing the NASA database.")
        return redirect("/planets/search")


    return render_template("results.html", planets = resp.json(), parameters=parameters, page=page)

@app.route("/planets/habitable")
def get_habitable_results():
    """Searches for and returns planets in habitable zone"""

    if not g.user:
        flash("You must be logged in.")
        return redirect("/")

    planets = []
    parameters = {}

    if session.get("PARAMETERS", None):
        parameters = session["PARAMETERS"]
    else:
        parameters = {"all": "on"}    
    
    search = ProcessSearch(parameters)        
    session["SEARCH"] = search.create_api_query()
    try:
        resp = requests.get(search.create_api_query())
    except ConnectionError:
        flash("There seems to be a problem accessing the NASA database.")
        return redirect("/planets/search")                                       

    for planet in resp.json():
        if planet['st_optmag'] and planet['st_dist'] and planet['st_spstr'] and planet['pl_orbsmax']:
            check_zone = HabitableZoneCheck(
                                        planet['st_optmag'], 
                                        planet['st_dist'], 
                                        planet['st_spstr'],
                                        planet['pl_orbsmax']
                                        )

            if check_zone.in_habitable_zone().value == "Habitable":
                planets.append(planet)                        

    return render_template("results.html", planets=planets, parameters=parameters, page=1)

@app.route("/password/email", methods=["GET", "POST"])
def show_enter_email():
    """Shows enter email form to reset password"""

    if g.user:
        return redirect(f"/users/{g.user.username}")

    form = EnterEmailForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email address doesn't exist")
            return redirect("/password/email")
        token = secrets.token_urlsafe(16)
        user.password_reset = token
        db.session.commit()

        msg = Message('Reset Password', sender = 'jeremiahbrem@gmail.com', recipients = [user.email])
        msg.body = """Cick on the link to reset your password:
                http://localhost:5000/password/reset?key=""" + token                  
        mail.send(msg)    

        return redirect(f"/password/check_email")

    return render_template("reset_pwd/enter_email.html", form=form)

@app.route("/password/check_email")    
def show_check_email():
    """Displays check email page"""

    if g.user:
        return redirect(f"/users/{g.user.username}")

    return render_template("reset_pwd/check_email.html")

@app.route("/password/reset", methods=["GET", "POST"])
def show_reset():
    """Displays reset password form after user clicks reset link in email"""

    if g.user:
        return redirect(f"/users/{g.user.username}")

    form = ResetPasswordForm()
    token = request.args.get("key")
    user = User.query.filter_by(password_reset=token).first()

    if form.validate_on_submit():
        password = form.password.data
        user.password = User.change_password(password)
        user.password_reset = None
        db.session.commit()
        flash("Password reset. Please login.")
        return redirect("/login")

    else:
        return render_template("reset_pwd/reset_password.html", form=form)    
