"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, jsonify
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy
from forms import CupcakeForm


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'thisisnotasecret'


connect_db(app)
db.create_all()
# Application routes *******************************************

@app.route('/')
def home_page():
    form = CupcakeForm()
    return render_template('home.html', form=form)



# APi Routes ***************************************************
@app.route('/api/cupcakes')
def list_cupcakes():
    cakes = [ c.serialize() for c in Cupcake.query.all()]
    return jsonify(cupcakes = cakes)


@app.route('/api/cupcakes/<int:id>')
def list_single_cupcake(id):
    cake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cake.serialize())


@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    data = request.json
    flavor = data['flavor']
    size = data['size']
    rating = data['rating']
    image = data.get('image')
    if image:
        cake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    else:
        cake = Cupcake(flavor=flavor, size=size, rating=rating)

    db.session.add(cake)
    db.session.commit()
    return (jsonify(cupcake = cake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def edit_cupcake(id):
    cake = Cupcake.query.get_or_404(id)
    data = request.json
    image = data.get('image')
    cake.flavor = data['flavor']
    cake.size = data['size']
    cake.rating = data['rating']
    if image:
        cake.image = image
    db.session.add(cake)
    db.session.commit()
    return (jsonify(cupcake = cake.serialize()), 200)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    try:
        Cupcake.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        return ({"error":"could not delete cupcake, try double checking id"},404)
    return {"message":"Cupcake deleted successfully"}
    