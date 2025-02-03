from datetime import datetime
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tourism_management_system"]
users_collection = db["users"]
flight_collection = db["flights"]
accommodation_collection = db["accommodations"]
bookings_collection = db["bookings"]

# Register a new user
def register_user(username, email, password, role):
    if users_collection.find_one({"email": email}):
        return False, "Email already exists"
    user = {
        "username": username,
        "email": email,
        "password": password,  
        "role": role,
        "created_at": datetime.utcnow(),
    }
    users_collection.insert_one(user)
    return True, "User registered successfully"

# Authenticate a user
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return True, user
    return False, None

# Add a flight to the database
def add_flight(departure, destination, date, airline, price, available_seats):
    try:
        date = datetime.combine(date, datetime.min.time())
        flight = {
            "departure": departure,
            "destination": destination,
            "date": date,
            "airline": airline,
            "price": price,
            "available_seats": available_seats,
            "created_at": datetime.utcnow(),
        }
        flight_id = flight_collection.insert_one(flight).inserted_id
        return flight_id
    except Exception as e:
        return f"An error occurred while adding the flight: {str(e)}"

# Add an accommodation to the database
def add_accommodation(name, location, price_per_night, check_in, check_out):
    try:
        check_in = datetime.combine(check_in, datetime.min.time())
        check_out = datetime.combine(check_out, datetime.min.time())
        accommodation = {
            "name": name,
            "location": location,
            "price_per_night": price_per_night,
            "check_in": check_in,
            "check_out": check_out,
            "created_at": datetime.utcnow(),
        }
        accommodation_id = accommodation_collection.insert_one(accommodation).inserted_id
        return accommodation_id
    except Exception as e:
        return f"An error occurred while adding the accommodation: {str(e)}"

# Search for flights based on criteria
def search_flights(departure, destination, date):
    try:
        date = datetime.combine(date, datetime.min.time())
        flights = flight_collection.find({"departure": departure, "destination": destination, "date": {"$gte": date}})
        return list(flights)
    except Exception as e:
        return f"An error occurred while searching for flights: {str(e)}"

# Search for accommodations based on criteria
def search_accommodations(destination, check_in_date, check_out_date):
    try:
        check_in_date = datetime.combine(check_in_date, datetime.min.time())
        check_out_date = datetime.combine(check_out_date, datetime.min.time())
        accommodations = accommodation_collection.find({
            "location": destination,
            "check_in": {"$lte": check_in_date},
            "check_out": {"$gte": check_out_date},
        })
        return list(accommodations)
    except Exception as e:
        return f"An error occurred while searching for accommodations: {str(e)}"

# Book a flight for a user
def book_flight(user_id, flight_id):
    if not user_id or not flight_id:
        return "Invalid user ID or flight ID"
    
    try:
        # Atomically find and update the flight document
        flight = flight_collection.find_one_and_update(
            {"_id": flight_id, "available_seats": {"$gt": 0}},  # Only update if seats are available
            {"$inc": {"available_seats": -1}},
            return_document=True
        )
        
        if not flight:  # If no flight was found or no available seats
            return "No available seats or flight does not exist"
        
        # Insert a new booking document
        bookings_collection.insert_one({
            "user_id": user_id,
            "flight_id": flight_id,
            "status": "Booked",
            "created_at": datetime.utcnow(),
        })
        
        return "Flight booked successfully!"
    except Exception as e:
        return f"An error occurred while booking the flight: {str(e)}"

# Book an accommodation for a user
def book_accommodation(user_id, accommodation_id):
    if not user_id or not accommodation_id:
        return "Invalid user ID or accommodation ID"
    
    try:
        accommodation = accommodation_collection.find_one({"_id": accommodation_id})
        if not accommodation:
            return "Accommodation not found"
        
        bookings_collection.insert_one({
            "user_id": user_id,
            "accommodation_id": accommodation_id,
            "status": "Booked",
            "created_at": datetime.utcnow(),
        })
        return "Accommodation booked successfully!"
    except Exception as e:
        return f"An error occurred while booking the accommodation: {str(e)}"
