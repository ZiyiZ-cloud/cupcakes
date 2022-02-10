"""Flask app for Cupcakes"""


from sqlalchemy import null
from flask import Flask, render_template, request, redirect, jsonify
from models import db, connect_db, Cupcake
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a dessert SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cupcakes')
def list_all():
    
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]
    
    return jsonify(cupcakes = serialized)

@app.route('/cupcakes', methods=['POST'])
def create_cupcake():
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    
    new_cupcake = Cupcake(flavor = flavor, size = size, rating= rating, image= image)

    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = serialize_cupcake(new_cupcake)
    
    return (jsonify(cupcake = serialized),201)


@app.route('/cupcakes/<cupcake_id>')
def list_single(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcake(cupcake)
    
    return jsonify(cupcake = serialized)


@app.route('/cupcakes/<cupcake_id>', methods = ['PATCH'])
def edit_single(cupcake_id):
    
    cupcake = Cupcake.query.get(cupcake_id)
    
    cupcake.flavor = request.json['flavor', cupcake.flaovr]
    cupcake.size = request.json['size', cupcake.size]
    cupcake.rating = request.json['rating', cupcake.rating]
    cupcake.image = request.json['image', cupcake.image]
    
    db.session.commit()
    serialized = serialize_cupcake(cupcake)
    
    return (jsonify(cupcake = serialized))

@app.route('/cupcakes/<cupcake_id>', methods = ['DELETE'])
def delete_single(cupcake_id):
    cupcake = Cupcake.quer.get(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = 'deleted')


