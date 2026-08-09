# Scalify - web app verzija
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scalify.db'

db = SQLAlchemy(app)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    object_type = db.Column(db.String(50), nullable=False)
    x = db.Column(db.Float, default=0)
    y = db.Column(db.Float, default=0)
    z = db.Column(db.Float, default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    object_type = db.Column(db.String(50), nullable=False)
    x = db.Column(db.Float, default=0)
    y = db.Column(db.Float, default=0)
    z = db.Column(db.Float, default=0)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/objects', methods=['GET'])
def objects():
    objects = Object.query.all()
    return render_template('objects.html', objects=objects)

@app.route('/objects/add', methods=['POST'])
def dodavanje():
    name = request.form['name']
    object_type = request.form['object_type']
    novi_objekt = Object(
        name=name,
        object_type=object_type
    )
    db.session.add(novi_objekt)
    db.session.commit()

    return redirect(url_for('objects'))

@app.route('/objects/delete/<int:id>', methods=['POST'])
def brisanje(id):
    objekt = Object.query.get_or_404(id)
    db.session.delete(objekt)
    db.session.commit()
    return redirect(url_for('objects'))

@app.route('/objects/edit/<int:id>', methods=['GET'])
def edit_object(id):
    objekt = Object.query.get_or_404(id)
    return objekt.id

@app.route('/objects/edits/<int:id>', methods=['PUT'])
def update_object(id):
    objekt = Object.query.get_or_404(id)

    objekt.name = request.form['name']
    objekt.object_type = request.form['object_type']
    objekt.x = request.form['x']
    objekt.y = request.form['y']
    objekt.z = request.form['z']

@app.route('/objects/<int:id>/save-model', methods=['POST'])
def spremi_model(id):
    objekt = Object.query.get_or_404(id)
    model = Model(
        name=objekt.name,
        object_type=objekt.object_type,
        x=objekt.x,
        y=objekt.y,
        z=objekt.z
    )

    db.session.add(model)
    db.session.commit()

    return redirect(url_for('modeling'))

@app.route('/modeling', methods=['GET'])
def modeling():
    models = Model.query.all()
    return render_template('modeling.html', models=models)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080) 