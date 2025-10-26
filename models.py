from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the SQLAlchemy object here so models can be imported without
# depending on app being fully initialized (avoids circular imports).
db = SQLAlchemy()

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    weapon_type = db.Column(db.String(30), nullable=False)  # AEG, GBB, Spring, etc.
    fps = db.Column(db.Integer, nullable=True)
    joules = db.Column(db.Float, nullable=True)
    is_tuned = db.Column(db.Boolean, default=False, nullable=False)
    purchase_date = db.Column(db.Date, nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with modules
    modules = db.relationship('Module', backref='weapon', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Weapon {self.brand} {self.model}>'

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    module_type = db.Column(db.String(30), nullable=False)  # Optics, Grip, Barrel, etc.
    brand = db.Column(db.String(50), nullable=True)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    purchase_date = db.Column(db.Date, nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to weapon (optional - modules can exist without being assigned)
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapon.id'), nullable=True)
    
    def __repr__(self):
        return f'<Module {self.name}>'
