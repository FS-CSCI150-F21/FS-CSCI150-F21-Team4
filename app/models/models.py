# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    password = db.Column(db.String(192),  nullable=False)
    
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)

    labor   = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    
    location   = db.Column(db.String(128),  nullable=False)

    description = db.Column(db.String(800),  nullable=False)

    projDescription = db.Column(db.String(800),  nullable=False)



    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, password, email, labor, 
        location, description, projDescription):


        self.name     = name
        self.password = password
        self.email = email
        self.labor = labor
        self.location = location
        self.description = description
        self.projDescription = projDescription


    def __repr__(self):
        return '<User %r>' % (self.name)   

