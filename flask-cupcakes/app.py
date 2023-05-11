from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'its-a-secret'

connect_db(app)

@app.route('/')
def home_page():
    """Home page of cupcake list"""

    return render_template("home.html")

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON with all cupcakes"""

    cupcake = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    """Info about a single cupcake"""

    cupcake = Cupcake.get.query_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake and return JSON"""

    data = request.json

    new_cupcake = Cupcake(flavor=data['flavor'],
                          size=data['size'],
                          rating=data['rating'],
                          image=data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(new_cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Updates a single cupcakes and responds with JSON"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete all info about a single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
