"""SQLAlchemy models for Exoplanet App."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Site user data"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_reset = db.Column(db.Text)

    lists = db.relationship("List", cascade="delete", single_parent=True)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, email, password, first_name, last_name):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def change_password(cls, new_password):
        """Hashes and updates new password"""

        return bcrypt.generate_password_hash(new_password).decode('UTF-8')

class List(db.Model):
    """User list data"""

    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(
                                        "users.id",
                                        ondelete="cascade"),
                                        nullable=False
                                        )

    user = db.relationship("User")
    favorites = db.relationship("Favorite", cascade="delete", single_parent=True)

    def __repr__(self):
        return f"<List #{self.id}: {self.name}>"

class Favorite(db.Model):
    """List item for favorited planet"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey(
                                        "lists.id",
                                        ondelete="cascade"
                                        ), 
                                        nullable=False
                                        )

    planet_name = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text)

    fav_list = db.relationship("List")

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)    