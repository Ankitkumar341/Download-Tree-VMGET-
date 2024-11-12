from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from dotenv import load_dotenv
from downloaders.youtube import YouTubeDownloader
from downloaders.instagram import InstagramDownloader
from downloaders.pinterest import PinterestDownloader
from models.user import User, db
from models.download import Download

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vmget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

db.init_app(app)

with app.app_context():
    db.create_all()

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['JWT_SECRET_KEY'])
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Download routes
@app.route('/api/download/youtube', methods=['POST'])
def youtube_download():
    data = request.get_json()
    downloader = YouTubeDownloader()
    try:
        result = downloader.download(data['url'], data['format'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download/instagram', methods=['POST'])
def instagram_download():
    data = request.get_json()
    downloader = InstagramDownloader()
    try:
        result = downloader.download(data['url'], data['type'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download/pinterest', methods=['POST'])
def pinterest_download():
    data = request.get_json()
    downloader = PinterestDownloader()
    try:
        result = downloader.download(data['url'], data['quality'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)