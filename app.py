from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Favorite, List
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///exoplanets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "s8t64h5gs3h1sdf35h4s"

connect_db(app)

db.drop_all()
db.create_all()

where = ""

resp = requests.get(f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&{where}&format=json")
print(resp.json())