# BookMySeat - A Django-Powered Movie Ticket Booking Platform

[![Deployment](https://img.shields.io/badge/Render-Deployed-brightgreen?style=for-the-badge&logo=render)](https://bookmyshow-web-e71k.onrender.com/)

**Live Project URL:** [**https://bookmyshow-web-e71k.onrender.com/**](https://bookmyshow-web-e71k.onrender.com/)

A comprehensive clone of the popular BookMyShow website, built from scratch with Python and Django. This application provides a full end-to-end user experience, from browsing movies and selecting seats to processing payments and receiving email confirmations.

---

## 📸 Screenshots

* **Homepage:** Users can browse recommended movies, live events, and premieres.
    
* **Movie Details:** Shows movie posters, descriptions, trailers, and filters for future showtimes.
* **User Profile:** A dedicated dashboard for users to manage their details and view their booking history.
* **Booking History:** Booked tickets (including seat numbers) appear on the user's profile.
* **Cloudinary Integration:** All uploaded media is successfully hosted on Cloudinary.

---

## ✨ Features

* **User Authentication:** Secure user registration, login, logout, and password reset functionality.
* **Dynamic Movie Listings:** Homepage and movie list pages that pull all movie data directly from the PostgreSQL database.
* **Showtime Filtering:** Theater and showtime lists are automatically filtered to show only upcoming events (`time__gte=timezone.now()`).
* **Interactive Seat Selection:** A visual interface for users to select seats for a specific showtime.
* **Payment Gateway:** Full integration with the **PayU** test gateway for processing payments.
* **Booking Confirmation & History:** Upon successful payment, seats are marked as "BOOKED," and the booking record appears on the user's profile.
* **Email Confirmation:** Automatically sends a detailed booking confirmation email to the user upon successful payment, using the **SendGrid** API for reliable delivery.
* **Cloudinary Media Storage:** All user-uploaded media (movie posters, profile pictures) is hosted on Cloudinary, separate from the application server.
* **Direct Image Uploads:** A robust custom solution for uploading profile pictures and movie posters directly to Cloudinary, bypassing the limitations of standard `model.save()` in a production environment.

---

## 🚀 Technology Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.12, Django 5.x, Gunicorn |
| **Frontend** | HTML5, CSS3, Bootstrap 4, JavaScript |
| **Database** | PostgreSQL (Production), SQLite3 (Development) |
| **Deployment** | Render |
| **Media Storage** | Cloudinary |
| **Email Service** | SendGrid API |
| **Payment Gateway**| PayU |
| **Core Libraries** | `django-cloudinary-storage`, `django-sendgrid-v5`, `whitenoise` |

---

## 🛠️ Local Setup & Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MangeshPhulari/django-bookmyshow.git](https://github.com/MangeshPhulari/django-bookmyshow.git)
    cd django-bookmyshow
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the project root (`bookmyshow/`) and add your environment variables:
    ```ini
    SECRET_KEY='your_django_secret_key'
    DEBUG=True

    # Database (can use default SQLite for local)
    DATABASE_URL='sqlite:///db.sqlite3'

    # Cloudinary
    CLOUDINARY_URL='cloudinary://api_key:api_secret@cloud_name'

    # SendGrid (for email)
    SENDGRID_API_KEY='SG.your_api_key'
    SENDGRID_FROM_EMAIL='your_verified@email.com'

    # PayU (Test Keys)
    PAYU_MERCHANT_KEY='your_payu_key'
    PAYU_MERCHANT_SALT='your_payu_salt'
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser** to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The project will be available at `http://127.0.0.1:8000/`.

---

## ☁️ Production Deployment & Challenges Solved

This project was successfully deployed to **Render**. The transition from `DEBUG=True` (local) to `DEBUG=False` (production) introduced several major challenges that were systematically debugged and resolved.

### 1. Static & Media Files
* **Static Files (CSS/JS):** `Whitenoise` was implemented to serve static files collected by `collectstatic`.
* **Media Files (Images):** `django-cloudinary-storage` was configured. The key challenge was that standard `model.save()` calls were failing to upload images silently.
    * **Solution:** A direct upload workaround was implemented in `movies/admin.py` and `users/views.py`. This code uses `cloudinary.uploader.upload()` to force the upload and then manually saves the correct Cloudinary path (e.g., `profile_pics/image.png`) to the database using `queryset.update()`, bypassing the default save method's conflict.

### 2. 500 Server Errors
* **Problem:** The live site would crash with 500 errors on the homepage and movie detail pages.
* **Solution:** The error was traced to the `{% cloudinary_url %}` tag. It was crashing when trying to render an object that had no image (`movie.image.name` was `None`). This was fixed by adding `{% if movie.image and movie.image.name %}` checks in all templates (`home.html`, `movie_detail.html`, `profile.html`) to safely handle movies or profiles without images.

### 3. Email Confirmation Failures
* **Problem:** After booking, the app would crash with a 500 error due to a timeout from the Gmail SMTP server.
* **Solution:** The email backend was migrated to **SendGrid**.
    * This still resulted in a `403 Forbidden` error from the SendGrid API.
    * Logs showed the error: `"The from address does not match a verified Sender Identity."`
    * **Final Fix:** The `SENDGRID_FROM_EMAIL` address was verified in the SendGrid dashboard, and `movies/email_utils.py` was updated to explicitly use `from_email=settings.SENDGRID_FROM_EMAIL` in the `send_mail` function. This resolved all email errors.

---

## 📧 Booking Confirmation Note

When you successfully book a ticket, the system will send a confirmation email via SendGrid.

**Please note:** If you do not see the email in your inbox within a few minutes, **please check your Spam or Junk folder.**

---

## 👨‍💻 Author

**Mangesh Phulari**
* GitHub: [@MangeshPhulari](https://github.com/MangeshPhulari)
