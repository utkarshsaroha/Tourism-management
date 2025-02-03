import streamlit as st
from datetime import datetime
from bson.objectid import ObjectId  # Import ObjectId to query MongoDB using _id
from backend import (
    register_user,
    authenticate_user,
    add_flight,
    add_accommodation,
    search_flights,
    search_accommodations,
    book_flight,
    book_accommodation,
    bookings_collection,
    flight_collection,
    accommodation_collection,
)

menu = ["Register", "Login", "Admin Panel", "Search Flights", "Search Accommodations", "User Bookings"]
choice = st.sidebar.selectbox("Menu", menu)

st.title("Tourism Management System")

if choice == "Register":
    st.subheader("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["User", "Admin"])
    if st.button("Register"):
        if username and email and password:
            success, message = register_user(username, email, password, role)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("All fields are required!")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            success, user = authenticate_user(username, password)
            if success:
                st.session_state["user"] = user
                st.success(f"Welcome {user['username']} ({user['role']})")
            else:
                st.error("Invalid username or password")
        else:
            st.error("Both username and password are required!")

elif choice == "Admin Panel":
    if "user" in st.session_state and st.session_state["user"]["role"] == "Admin":
        admin_task = st.selectbox("Admin Tasks", ["Add Flights", "Add Accommodations"])
        if admin_task == "Add Flights":
            departure = st.text_input("Departure")
            destination = st.text_input("Destination")
            date = st.date_input("Date")
            airline = st.text_input("Airline")
            price = st.number_input("Price", min_value=0.0)
            available_seats = st.number_input("Seats", min_value=1)
            if st.button("Add Flight"):
                if departure and destination and date and airline:
                    flight_id = add_flight(departure, destination, date, airline, price, available_seats)
                    st.success(f"Flight Added! Flight ID: {flight_id}")
                else:
                    st.error("All fields are required!")
        elif admin_task == "Add Accommodations":
            name = st.text_input("Accommodation Name")
            location = st.text_input("Location")
            price_per_night = st.number_input("Price per Night", min_value=0.0)
            check_in = st.date_input("Check-In")
            check_out = st.date_input("Check-Out")
            if st.button("Add Accommodation"):
                if name and location and check_in and check_out:
                    accommodation_id = add_accommodation(name, location, price_per_night, check_in, check_out)
                    st.success(f"Accommodation Added! Accommodation ID: {accommodation_id}")
                else:
                    st.error("All fields are required!")
    else:
        st.error("Access denied! Admins only.")

elif choice == "Search Flights":
    if "user" in st.session_state:  
        st.subheader("Search Flights")
        departure = st.text_input("Departure")
        destination = st.text_input("Destination")
        date = st.date_input("Date")
        if st.button("Search Flights"):
            if departure and destination and date:
                flights = search_flights(departure, destination, date)
                if flights:
                    for flight in flights:
                        st.write(f"Flight ID: {flight['_id']} | {flight['airline']} | {flight['departure']} -> {flight['destination']} | Price: ${flight['price']} | Seats Available: {flight['available_seats']}")
                else:
                    st.error("No flights found for the given criteria.")
            else:
                st.error("All fields are required!")
    else:
        st.error("Please log in to search for flights.")

elif choice == "Search Accommodations":
    if "user" in st.session_state:  
        st.subheader("Search Accommodations")
        destination = st.text_input("Destination")
        check_in_date = st.date_input("Check-In Date")
        check_out_date = st.date_input("Check-Out Date")
        if st.button("Search Accommodations"):
            if destination and check_in_date and check_out_date:
                accommodations = search_accommodations(destination, check_in_date, check_out_date)
                if accommodations:
                    for accommodation in accommodations:
                        st.write(f"Accommodation ID: {accommodation['_id']} | {accommodation['name']} | Location: {accommodation['location']} | Price per Night: ${accommodation['price_per_night']}")
                else:
                    st.error("No accommodations found for the given criteria.")
            else:
                st.error("All fields are required!")
    else:
        st.error("Please log in to search for accommodations.")

elif choice == "User Bookings":
    st.subheader("Your Bookings")
    if "user" in st.session_state:
        user_id = st.session_state["user"]["_id"]
        
        flight_id = st.text_input("Enter Flight ID to Book:")
        if flight_id and st.button("Book Flight"):
            try:
                result = book_flight(user_id, ObjectId(flight_id))
                st.success(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        accommodation_id = st.text_input("Enter Accommodation ID to Book:")
        if accommodation_id and st.button("Book Accommodation"):
            try:
                result = book_accommodation(user_id, ObjectId(accommodation_id))
                st.success(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        flight_bookings = bookings_collection.find({"user_id": user_id, "flight_id": {"$exists": True}})
        accommodation_bookings = bookings_collection.find({"user_id": user_id, "accommodation_id": {"$exists": True}})
        
        st.write("### Flight Bookings:")
        for booking in flight_bookings:
            flight = flight_collection.find_one({"_id": booking["flight_id"]})
            st.write(f"Flight ID: {booking['flight_id']} | {flight['departure']} -> {flight['destination']} | Status: {booking['status']}")
        
        st.write("### Accommodation Bookings:")
        for booking in accommodation_bookings:
            accommodation = accommodation_collection.find_one({"_id": booking["accommodation_id"]})
            st.write(f"Accommodation ID: {booking['accommodation_id']} | {accommodation['name']} | Location: {accommodation['location']} | Status: {booking['status']}")
    else:
        st.error("Please log in to view your bookings.")
