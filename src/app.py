"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorites

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        email=data['email'],
        password=data['password'],
        is_active=data['is_active'],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    return jsonify([character.serialize() for character in characters])

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    if character:
        return jsonify(character.serialize())
    else:
        return jsonify({'message': 'Character not found'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    else:
        return jsonify({'message': 'Planet not found'}), 404

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Characters.query.all()
    return jsonify([person.serialize() for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Characters.query.get(people_id)
    if person:
        return jsonify(person.serialize())
    else:
        return jsonify({'message': 'Person not found'}), 404

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    else:
        return jsonify({'message': 'Planet not found'}), 404

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.headers.get('user_id')
    
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites])

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.headers.get('user_id')
    
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404
    
    favorite = favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet added successfully'})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.headers.get('user_id')
    
    person = Characters.query.get(people_id)
    if not person:
        return jsonify({'message': 'Person not found'}), 404
    
    favorite = favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite person added successfully'})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.headers.get('user_id')

    favorite = favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'message': 'Favorite planet not found'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.headers.get('user_id')

    favorite = favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({'message': 'Favorite person not found'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite person deleted successfully'})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
