from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_characters = db.Table(
    "favorite_characters",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("character_id", db.ForeignKey("characters.id")),
)
favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("planets_id", db.ForeignKey("planets.id")),
)

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_characters= db.relationship("Characters",secondary=favorite_characters)
    favorite_planets= db.relationship("Planets",secondary=favorite_planets)


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": [x.serialize() for x in self.favorite_characters],
            "favorite_planets":[x.serialize() for x in self.favorite_planets],

            # do not serialize the password, its a security breach
        }
    


class Characters(db.Model):
    __tablename__= "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String (60), unique=False, nullable=False)
    gender = db.Column (db.String(60), unique=False, nullable=False)
    birth_year = db.Column (db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year":self.birth_year,

            # do not serialize the password, its a security breach
        }
    


class Planets(db.Model):
    __tablename__= "planets"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    terrain= db.Column(db.String(100), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.name,
            "climate": self.climate,
            "terrain": self.terrain,


            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'people_id': self.people_id,
        }