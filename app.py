from flask import Flask, render_template,session, request, redirect, jsonify,g
from sqlalchemy import desc
from helpers import  login_required
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miniParking.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)



# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    hash = db.Column(db.String, nullable=False)

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "username")

# Brand Model
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    sorting = db.Column(db.Integer, default=0)

class BrandSchema(ma.Schema):
    class Meta : 
        model = Brand
        fields = ("id", "name", "sorting")


# DiscountCard Model
class DiscountCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.String, nullable=False)
    percentage = db.Column(db.REAL, nullable=False)

class DiscountCardSchema(ma.Schema):
    class Meta : 
        model= DiscountCard
        fields = ("id", "customer","percentage")

# VehicleType Model
class VehicleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)


class VehicleTypeSchema(ma.Schema):
    class Meta:
        model = VehicleType
        fields = ("id", "type")

# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    isUsed = db.Column(db.Integer, default=0)
    isHidden = db.Column(db.Integer, default=0)

class LocationSchema(ma.Schema):
    class Meta:
        model= Location
        fields = ("id", "name","isUsed")

# CheckIn Model
class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, db.ForeignKey('vehicle_type.id'), nullable=False)
    number = db.Column(db.String, nullable=False)
    creationTime = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    discount = db.Column(db.Integer, db.ForeignKey('discount_card.id'), nullable=False)
    brand = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

class CheckInSchema(ma.Schema):
    class Meta:
        model= CheckIn
        fields = ("id", "type","number","creationTime","discount","brand")

# CheckOut Model
class CheckOut(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkInId = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)
    isPaid = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.REAL)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class CheckOutSchema(ma.Schema):
    class Meta:
        model= CheckOut 
        fields = ("id", "checkInId","isPaid","amount","createdOn")

# Move Model
class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkInId = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)
    fromLocationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    toLocationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    moveTime = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class MoveSchema(ma.Schema):
    class Meta:
        model= Move
        fields = ("id", "checkInId","fromLocationId","toLocationId","moveTime")



secret_key = secrets.token_hex(16)
app.secret_key = 'd127b18e-6524-4e9f-a65c-9c7d83d02a80'

def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created  successfully.")
        except Exception as e:
            print("An error occurred while creating database tables:", e)


@app.route('/', methods = ['GET'])
@login_required
def get():
    if request.method == "GET":

        # q = (db.session.query(CheckIn, Location, VehicleType,DiscountCard, Move,Brand)
        # .select_from(CheckIn)
        # .outerjoin(Move, (Move.fromLocationId == Location.id | Move.toLocationId == Location.id))
        # .join(Location)
        # .join(VehicleType)
        # .join(DiscountCard)
        # .join(Brand)
        # .filter(Location.isUsed == 0)
        # .order_by(desc(CheckIn.creationTime))
        # ).all()

        # print(q)
         
        return render_template('index.html')
    # return jsonify({'msg' : 'hellos world'})


@app.route("/arrivalReport")
def arrivalReport():
    return render_template('arrivalHistory.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    try:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            userName = request.form.get("username")
            password = request.form.get("password")

            # Ensure username was submitted
            if not userName:
                return jsonify({"error": "Must provide username."}), 400

            # Ensure password was submitted
            elif not password:
                return jsonify({"error": "Must provide password."}), 400

            existingUser: User = User.query.filter_by(username = userName).first()

            if not existingUser or not  check_password_hash(existingUser.hash, password):
                return jsonify({"error": "Username and password did not match."}), 400
         
            session["user_id"] = existingUser.id

            # Redirect user to home page
            return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("login.html")

    except Exception as e:
        # Handle the exception and return an error response
        return jsonify({"error": str(e)}), 500



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        try:
            userName = request.form.get("username")
            password = request.form.get("password")
            confirmPassword = request.form.get("confirmation")
            
            # Ensure username was submitted
            if not userName:
                return jsonify({"error": "Invalid username."}), 400
            # Ensure password was submitted
            elif not password:
                return jsonify({"error": "Invalid password."}), 400
            # Ensure password and confirmation match
            elif password != confirmPassword:
                return jsonify({"error": "Password and confirm password do not match."}), 400


            hashedPassword = generate_password_hash(password, method="pbkdf2", salt_length=16)
            user = User(username = userName, hash = hashedPassword)
            db.session.add(user)
            db.session.commit()
       
            return render_template("login.html")
         
        except Exception as e:
            logging.debug(f"error is {e}")
            return jsonify({"error": str(e)}), 500


    else:
        return render_template("register.html")


@app.route("/checkIn", methods = ["POST"])
def checkIn():
    
    if request.method == "POST":
        try:
            type = request.form.get("type")
            brand = request.form.get("brand")
            number = request.form.get("number")
            location = request.form.get("location")
            discount = request.form.get("discount")

            if not number or not type or not brand or not location or not discount:
                 return jsonify({"error": "Please provide valid input."}), 400  

            checkIn = CheckIn(type = type, number = number, discount = discount, brand = brand)

            db.session.add(checkIn)
            db.session.commit()

            transit : Location = findLocationTransit()    

            inMove : Move = Move(checkInId = checkIn.id, fromLocationId = transit.id, toLocationId = location)
            db.session.add(inMove)

            location_to_update: Location = Location.query.get(location)

            if location_to_update:
                location_to_update.isUsed = 1

            db.session.commit()

           
         
        except Exception as e:
            logging.debug(f"error is {e}")
            return jsonify({"error": str(e)}), 500


        



@app.route("/checkInDatas", methods= ["GET"])
@login_required
def getCheckInData():
    if(request.method == "GET"):
        empty_locations = LocationSchema(many=True).dump(load_empty_locations()) 
        brands = BrandSchema(many=True).dump(load_brand())
        types = VehicleTypeSchema(many=True).dump(load_VehicleType()) 
        discounts = DiscountCardSchema(many=True).dump(load_Discount())

        data_dict = {
            "empty_locations" : empty_locations,
            "brands" : brands,
            "types" : types,
            "discounts" : discounts
        }

        return jsonify(data_dict);



@login_required
def load_empty_locations():
    empty_location =  Location.query.filter_by(isUsed = 0).all()
    if len(empty_location) == 0 :
        return jsonify({"error": "All locations are occupied.Please check out vehicle."}), 400
    
    return empty_location

@login_required
def load_brand():
    brand =  Brand.query.all()
    if len(brand) == 0 :
        return jsonify({"error": "Brand not found."}), 400
    return brand

@login_required
def load_VehicleType():
    type =  VehicleType.query.all()
    if len(type) == 0 :
        return jsonify({"error": "vehicle type not found."}), 400
    
    return type

@login_required
def load_Discount():
    discount = DiscountCard.query.all()
    if len(discount) == 0:
        return jsonify({"error": "Discount not found."}), 400
    
    return discount

@login_required
def findLocationTransit():
    transitLocation: Location = Location.query.filter_by(isHidden = 1).first();
    return transitLocation







if __name__ == '__main__':
    init_db()
    app.run(debug=True)