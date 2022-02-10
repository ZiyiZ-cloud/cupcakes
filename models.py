"""Models for Cupcake app."""

from sqlalchemy import true
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

default_time = datetime.now()

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class Cupcake(db.Model):
    """User."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.String,
                     nullable=False,
                     )
    size = db.Column(db.String,
                     nullable=False,
                     )
    rating = db.Column(db.Float,
                       nullable = False)
    image = db.Column(db.Text,
                          nullable= False,
                          default = DEFAULT_IMAGE_URL)
    