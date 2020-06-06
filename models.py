"""SQLAlchemy models for Exoplanet App."""

class Planet(db.Model):
    """Exoplanet data"""

    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mass = db.Column(db.Float)
    radius = db.Column(db.Float)
    orbit = db.Column(db.Float)
    habitable_zone = db.Column(db.Boolean)
    star_id = db.Column(db.Integer, db.ForeignKey("stars.id"), nullable=False)

    star = db.relationship('Star', backref="planets")

class Star(db.Model):
    """Host star data"""

    __tablename__ = "stars"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mass = db.Column(db.Float)
    radius = db.Column(db.Float)
    luminosity = db.Column(db.Float)
    optical_mag = db.Column(db.Float)
    distance = db.Column(db.Float)
    temp = db.Column(db.Float)

class User(db.Model):
    """Site user data"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

class List(db.Model):
    """User list data"""

    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="lists")
    planets = db.relationship("Planet", secondary="favorites")

class Favorite(db.Model):
    """Maps user list to favorited planets"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    photo = db.Column(db.Text)