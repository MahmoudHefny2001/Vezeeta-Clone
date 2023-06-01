# Vezeeta Clone

This is a Vezeeta clone, a web application built with Django, that allows users to book medical appointments online. It provides a platform for users to search for doctors, view their profiles and available time slots, and book appointments conveniently.

## Features

- User Registration: Users can create an account to access the booking functionality.
- Doctor Search: Users can search for doctors based on various criteria such as specialization, location, and availability.
- Doctor Profiles: Detailed profiles are provided for each doctor, including their qualifications, experience, and available time slots.
- Appointment Booking: Users can book appointments with their chosen doctors by selecting a suitable time slot.
- Appointment Management: Users can view and manage their booked appointments, including rescheduling or canceling them if necessary.

## Installation

1. Clone the repository:

    https://github.com/MahmoudHefny2001/Vezeeta-Clone

## Navigate to the project directory:
    cd Vezeeta-Clone

## Create and activate a virtual environment (optional but recommended):
    python3 -m venv env
    . env/bin/activate

## Install the dependencies:
    pip3 install -r requirements.txt

## Set up the database:
    python3 manage.py makemigrations
    python3 manage.py migrate


## Run the development server:
    python3 manage.py runserver

## Access the application in your web browser at http://localhost:8000.

Configuration
Database: By default, the application is configured to use a SQLite database. But I used a different database (PostgreSQL), update the DATABASES setting in the settings.py file.

Static and Media Files: The application utilizes Django's built-in static and media file handling. Make sure to set up the appropriate storage settings and configure your web server to serve the static and media files in a production environment.

Secret Key: In production, generate a secure secret key and update the SECRET_KEY setting in the settings.py file. You can use the django.core.management.utils.get_random_secret_key() function to generate a new secret key.

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


Acknowledgements
This project is inspired by Vezeeta, an online medical appointment booking platform. Special thanks to the Django community for their excellent documentation and resources.

Contact
For any inquiries or questions, please contact hefny4@gmail.com.
