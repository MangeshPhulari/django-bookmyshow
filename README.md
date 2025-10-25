# Django BookMyShow Clone 🎬🎟️

A web application replicating core features of BookMyShow, built using Python and Django. This project allows users to browse movies, view details and trailers, select theaters and showtimes, book seats, and process payments (using PayU test gateway).

---

## ✨ Features

* **Movie Browsing:** View a list of movies with images and basic details.
* **Filtering & Searching:** Filter movies by **Genre** and **Language**, and search by **Title** or **Cast**.
* **Movie Details:** View detailed information about a movie, including description, cast, release date, and official rating.
* **YouTube Trailer Integration:** Watch embedded YouTube trailers directly on the movie detail page.
* **Theater & Showtime Listing:** See available theaters and showtimes for a selected movie.
* **Seat Selection:** Interactive seat map showing available, booked, and reserved seats.
* **User Authentication:** User registration, login, logout, and password reset functionality.
* **User Profiles:** View profile details, update username/email, and upload a profile picture.
* **Booking History:** Logged-in users can view their past bookings on their profile page.
* **Temporary Seat Reservation:** Selected seats are **reserved for 5 minutes** during checkout, with a countdown timer. Seats are automatically released if payment isn't completed.
* **PayU Payment Gateway Integration:** Simulate payment processing using PayU's test environment.
* **Email Confirmation:** Receive booking confirmation emails upon successful payment.
* **Movie Reviews:** Logged-in users can submit ratings (1-5) and comments for movies. Average user ratings are displayed.
* **Responsive Design:** User interface adapted for various screen sizes using Bootstrap 4.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap 4, JavaScript
* **Database:** SQLite (for development), PostgreSQL (recommended for production)
* **Payment Gateway:** PayU (Test Environment)
* **Email:** Django SMTP Email Backend (e.g., using Gmail)
* **Environment Variables:** python-decouple
* **Image Handling:** Pillow
* **Others:** shortuuid (for unique IDs)

---

## 🚀 Local Setup & Installation

Follow these steps to get the project running on your local machine.

1.  **Prerequisites:**
    * Python 3.9+ ([Download Python](https://www.python.org/downloads/))
    * `pip` (Python package installer)
    * Git ([Download Git](https://git-scm.com/downloads/))
    * (Optional but Recommended) A virtual environment tool (`venv`)

2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/MangeshPhulari/django-bookmyshow.git](https://github.com/MangeshPhulari/django-bookmyshow.git) # Your actual repo URL
    cd django-bookmyshow
    ```

3.  **Create and Activate Virtual Environment:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Environment Variables:**
    * Create a file named `.env` in the project root directory (same level as `manage.py`).
    * Add the necessary environment variables (see section below).

6.  **Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Create Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    (Follow the prompts to create an admin account)

8.  **Run Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application will be accessible at `http://127.0.0.1:8000/`.

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following variables:

```ini
# Django
SECRET_KEY='your_strong_secret_key_here' # Generate a strong random key
DEBUG=True # Set to False in production
# DATABASE_URL='your_database_connection_url' # Optional for local SQLite, required for production DB

# Email (Example using Gmail App Password)
EMAIL_USER='your_email@gmail.com'
EMAIL_PASS='your_gmail_app_password' # Use an App Password if using Gmail 2FA

# PayU Test Credentials
PAYU_MERCHANT_KEY='YBAGb3' # Your PayU test key
PAYU_MERCHANT_SALT='M4duwyt7y2AO5xS3nuBIzBPKPCO12MWU' # Your PayU test salt