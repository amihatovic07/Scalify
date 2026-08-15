# Scalify - web app verzija
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import secrets
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps


app = Flask(__name__)
@app.after_request
def dodaj_sigurnosne_headere(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "connect-src 'self';"
    )
    return response

app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scalify.db'

db = SQLAlchemy(app)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

load_dotenv()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# dekorator koji blokira rutu ako korisnik nije admin (provjerava Flask sesiju)
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return {'status': 'error', 'message': 'Unauthorized'}, 403
        return f(*args, **kwargs)
    return wrapper

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    object_type = db.Column(db.String(50), nullable=False)
    dimension = db.Column(db.Integer, nullable=False, default=3)  # 2 = XY, 3 = XYZ
    points = db.relationship('Point', backref='object', cascade='all, delete-orphan')

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'), nullable=False)
    point_index = db.Column(db.Integer, nullable=False)  # redoslijed točke (0, 1, 2...)
    x = db.Column(db.Float, default=0)
    y = db.Column(db.Float, default=0)
    z = db.Column(db.Float, nullable=True)  # null ako je dimension=2

# this class will be used in future to enable the usage for multiple users to login and insert scales for objects they want
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

@app.route('/api/posts', methods=['GET'])
def api_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return {
        'posts': [
            {
                'id': p.id,
                'title': p.title,
                'content': p.content,
                'created_at': p.created_at.strftime('%d.%m.%Y %H:%M')
            } for p in posts
        ]
    }

@app.route('/api/posts', methods=['POST'])
@admin_required
def add_post():
    data = request.get_json()
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return {'status': 'ok', 'id': post.id}

@app.route('/api/posts/<int:id>', methods=['PUT'])
@admin_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return {'status': 'ok'}

@app.route('/api/posts/<int:id>', methods=['DELETE'])
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return {'status': 'ok'}

@app.route('/api/admin/login', methods=['POST'])
@limiter.limit("5 per minute")
def admin_login():
    data = request.get_json()
    password = data.get('password', '')
    expected = os.environ.get('ADMIN_PASSWORD')
    if password == os.environ.get('ADMIN_PASSWORD'):
        session['is_admin'] = True
        return {'status': 'ok'}
    else:
        return {'status': 'error', 'message': 'Wrong password'}, 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    return {'status': 'ok'}

@app.route('/api/admin/status', methods=['GET'])
def admin_status():
    return {'is_admin': session.get('is_admin', False)}

@app.route('/objects', methods=['GET'])
def objects():
    objects = Object.query.all()
    return render_template('objects.html', objects=objects)

@app.route('/api/objects', methods=['GET'])
def api_objects():
    objects = Object.query.all()
    return {
        'objects': [
            {
                'id': o.id,
                'name': o.name,
                'object_type': o.object_type,
                'dimension': o.dimension,
                'points': [
                    {'index': p.point_index, 'x': p.x, 'y': p.y, 'z': p.z}
                    for p in sorted(o.points, key=lambda p: p.point_index)
                ]
            } for o in objects
        ]
    }

@app.route('/objects/add', methods=['POST'])
def dodavanje():
    data = request.get_json()
    novi_objekt = Object(
        name=data['name'],
        object_type=data['object_type'],
        dimension=int(data['dimension'])
    )
    db.session.add(novi_objekt)
    db.session.flush()  # da dobijemo novi_objekt.id prije commita

    for i, tocka in enumerate(data['points']):
        p = Point(
            object_id=novi_objekt.id,
            point_index=i,
            x=tocka['x'],
            y=tocka['y'],
            z=tocka.get('z') if novi_objekt.dimension == 3 else None
        )
        db.session.add(p)

    db.session.commit()
    return {'status': 'ok', 'id': novi_objekt.id}

@app.route('/objects/edit/<int:id>', methods=['GET'])
def edit_object(id):
    objekt = Object.query.get_or_404(id)
    return {
        'id': objekt.id,
        'name': objekt.name,
        'object_type': objekt.object_type,
        'dimension': objekt.dimension,
        'points': [
            {'index': p.point_index, 'x': p.x, 'y': p.y, 'z': p.z}
            for p in sorted(objekt.points, key=lambda p: p.point_index)
        ]
    }

@app.route('/objects/edit/<int:id>', methods=['PUT'])
def update_object(id):
    objekt = Object.query.get_or_404(id)
    data = request.get_json()
    objekt.name = data['name']
    objekt.object_type = data['object_type']
    objekt.dimension = int(data['dimension'])

    Point.query.filter_by(object_id=id).delete()

    for i, tocka in enumerate(data['points']):
        p = Point(
            object_id=id,
            point_index=i,
            x=tocka['x'],
            y=tocka['y'],
            z=tocka.get('z') if objekt.dimension == 3 else None
        )
        db.session.add(p)

    db.session.commit()
    return {'status': 'ok'}

@app.route('/objects/delete/<int:id>', methods=['DELETE'])
def brisanje(id):
    objekt = Object.query.get_or_404(id)
    db.session.delete(objekt)
    db.session.commit()
    return {'status': 'ok'}

@app.route('/objects/<int:id>/save-model', methods=['POST'])
def spremi_model(id):
    objekt = Object.query.get_or_404(id)
    model = Model(
        name=objekt.name,
        object_type=objekt.object_type
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