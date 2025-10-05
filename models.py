from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Relationship to movements
    movements = db.relationship('ProductMovement', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Location(db.Model):
    __tablename__ = 'location'
    
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    
    # Relationships to movements
    movements_from = db.relationship('ProductMovement', 
                                    foreign_keys='ProductMovement.from_location',
                                    backref='from_loc', 
                                    lazy=True)
    movements_to = db.relationship('ProductMovement', 
                                  foreign_keys='ProductMovement.to_location',
                                  backref='to_loc', 
                                  lazy=True)
    
    def __repr__(self):
        return f'<Location {self.name}>'


class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'
    
    def get_movement_type(self):
        """Determine the type of movement"""
        if self.from_location is None and self.to_location is not None:
            return "IN"
        elif self.from_location is not None and self.to_location is None:
            return "OUT"
        else:
            return "TRANSFER"