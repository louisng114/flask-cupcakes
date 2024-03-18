"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home_page():
    """display homepage"""

    cupcakes = Cupcake.query.all()

    return render_template("index.html", cupcakes=cupcakes)

@app.route("/api/cupcakes")
def cupcake_details():
    """get details for all cupcakes"""

    serialized = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_by_id(cupcake_id):
    """get cupcake details by id"""

    serialized = Cupcake.query.get_or_404(cupcake_id).serialize_cupcake()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """post new cupcake"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize_cupcake()

    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """patch (update) cupcake details"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit(cupcake_id)

    serialized = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """delete cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
