Overview

The Tourism Management System is a web-based application that simplifies travel planning by allowing users to register, search for flights and accommodations, and book them. It is built using Python, Streamlit, and MongoDB, offering a user-friendly interface and a scalable database system.

Features

1. User & Admin Roles

Users can register, search for flights/accommodations, and book them.

Admins can manage flights and accommodations (add new entries).

2. Search & Booking

Users can search flights and accommodations based on location, date, and price.

Real-time booking with instant confirmation.

3. Database Integration

MongoDB is used to store user details, flight/accommodation information, and bookings.

4. Streamlit Interface

An interactive and user-friendly web UI built using Streamlit.

Workflow

User Registration & Login

Users register with a username, email, and password.

Authentication ensures secure login and access control.

Admin Panel (Only for Admins)

Add new flights with details (departure, destination, date, price, seats, etc.).

Add new accommodations (name, location, price per night, availability, etc.).

Searching Flights & Accommodations

Users search based on criteria like departure, destination, date, or availability.

Booking System

Users can book flights/accommodations using unique IDs.

MongoDB updates seat availability and booking records dynamically.

User Dashboard

Users can view their current bookings for flights and accommodations.

Technologies Used

Frontend: Streamlit (Python-based UI framework)

Backend: Python with MongoDB integration (pymongo)

Database: MongoDB (NoSQL database for efficient storage)

Libraries:

pymongo (database connection)

datetime (handling date and time)

streamlit (web UI development)
MongoDB Setup

Ensure MongoDB is running locally or connect to an online MongoDB database.

Update backend.py with the correct MongoDB connection string.

Future Enhancements

Payment Integration – Add payment gateways for transactions.

Notifications – Send booking confirmations via email/SMS.

User Reviews & Ratings – Allow users to rate flights and accommodations.

Admin Dashboard – Analytics and booking trends for admins.
