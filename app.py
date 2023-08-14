from flask import Flask, render_template,session, request, redirect, jsonify,g
from sqlalchemy import desc, func, or_, text
from helpers import  login_required
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG
from datetime import datetime

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
    rate = db.Column(db.Integer, nullable= False)


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

        query = db.session.query(
        CheckIn.id,
        CheckIn.number,
        VehicleType.type,
        VehicleType.rate,
        Brand.name.label('brand'),
        Location.name,
        CheckIn.creationTime,
        DiscountCard.customer,
        DiscountCard.percentage

          # Calculate difference in hours


    ).join(
        VehicleType,
        VehicleType.id == CheckIn.type,
        isouter= True
    ).join(
        Brand,
        Brand.id == CheckIn.brand,
        isouter=True
    ).join(
        Move,
        Move.checkInId == CheckIn.id,
        isouter=True
    ).join(
        Location,
        Location.id == Move.toLocationId,
        isouter= True
    ).join(
        CheckOut,
        CheckOut.checkInId == CheckIn.id,    
        isouter= True
    ).join(
        DiscountCard,
        DiscountCard.id == CheckIn.discount,
        isouter= True
    ).order_by(CheckIn.creationTime.desc()).all()



        # .filter(or_(CheckOut.id == None, CheckOut.id.is_(None))).order_by(CheckIn.creationTime.desc()).all() 
    current_time = datetime.utcnow()
    summaryQuery = []
    print('query : ' ,len(query))
    for row in query:
        row_dict = {
            'id':row.id,
            'number': row.number,
            'type': row.type,
            'brand': row.brand,
            'location': row.name,
            'creationTime': row.creationTime,
            'customer': row.customer,
            'percentage': row.percentage,
            'rate': row.rate
        }
        hours_since_creation = (current_time - row.creationTime).total_seconds() / 3600
        row_dict['hour'] = 1 if 0 < hours_since_creation < 1 else int(hours_since_creation)
        totalFee = row.rate * row_dict['hour'] 
        row_dict['fee'] = totalFee * (1 - row.percentage/100)
        # property_names = row._fields
        # row_data = row._asdict()  # Convert Row to a dictionary
        # print(property_names)  # Print the property names for this row
        # print(row_data)  # Print the actual row data

        summaryQuery.append(row_dict)


         
    return render_template('index.html', summaryQuery = summaryQuery)
    # return jsonify({'msg' : 'hellos world'})


@app.route("/checkInReport")
def checkInReport():
    checkInsQuery = db.session.query(
        CheckIn.number,
        VehicleType.type,
        Brand.name.label('brand'),
        Location.name,
        CheckIn.creationTime,
        DiscountCard.customer,
        DiscountCard.percentage
    ).join(
        VehicleType,
        VehicleType.id == CheckIn.type,
        isouter= True
    ).join(
        Brand,
        Brand.id == CheckIn.brand,
        isouter=True
    ).join(
        Move,
        Move.checkInId == CheckIn.id,
        isouter=True
    ).join(
        Location,
        Location.id == Move.toLocationId,
        isouter= True
    ).join(
        DiscountCard,
        DiscountCard.id == CheckIn.discount,
        isouter= True
    ).order_by(CheckIn.creationTime.desc()).all() 
    
    for row in checkInsQuery:
        property_names = row._fields
        row_data = row._asdict()  # Convert Row to a dictionary
        print(property_names)  # Print the property names for this row
        print(row_data)  # Print the actual row data

    return render_template('checkInReport.html', checkInsQuery = checkInsQuery)

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
            
            existingVehicle : CheckIn = db.session.query(
                                    CheckIn.number,
                                    CheckIn.brand,
                                    
                                    ).join(
                                        CheckOut,
                                        CheckOut.checkInId == CheckIn.id,
                                        isouter= True
                                    ).filter(
                CheckOut.id == None,
                CheckIn.brand == brand,
                CheckIn.number == number
                
                
                ).first()   
            print(existingVehicle)
            if existingVehicle:
                return jsonify({"error": "Vehicle already in parking."}), 400

            checkIn = CheckIn(type = type, number = number, discount = discount, brand = brand)

            db.session.add(checkIn)
            db.session.commit()

            transit : Location = findLocationTransit()    

            inMove : Move = Move(checkInId = checkIn.id, fromLocationId = transit.id, toLocationId = location)
            db.session.add(inMove)

            db.session.commit()

            locationUpdate(location, 1)

            return jsonify({"message": "Check-in successful."}), 200
         
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
    empty_location =  Location.query.filter_by(isUsed = 0).filter_by(isHidden = 0).all()
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


@login_required
def locationUpdate(id, value):
    print(id, value)
    location_to_update: Location = Location.query.filter_by(id = id).first();

    if location_to_update:
            location_to_update.isUsed = value
            db.session.commit()





if __name__ == '__main__':
    init_db()
    app.run(debug=True)