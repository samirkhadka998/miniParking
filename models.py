from app import db  # Assuming you have initialized the SQLAlchemy instance in your Flask app (app.py)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    hash = db.Column(db.String, nullable=False)

# Brand Model
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    sorting = db.Column(db.Integer, default=0)

# DiscountCard Model
class DiscountCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.String, nullable=False)
    percentage = db.Column(db.REAL, nullable=False)

# VehicleType Model
class VehicleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)

# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    isUsed = db.Column(db.Integer, default=0)

# CheckIn Model
class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, db.ForeignKey('vehicle_type.id'), nullable=False)
    number = db.Column(db.String, nullable=False)
    creationTime = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    discount = db.Column(db.Integer, db.ForeignKey('discount_card.id'), nullable=False)
    brand = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

# CheckOut Model
class CheckOut(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkInId = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)
    isPaid = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.REAL)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp())

# Move Model
class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkInId = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)
    fromLocationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    toLocationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    moveTime = db.Column(db.DateTime, server_default=db.func.current_timestamp())

