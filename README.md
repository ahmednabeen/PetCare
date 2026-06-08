# PetCare

A Django-based pet adoption platform where users can browse pets by category, view details, and submit adoption applications.

## Features

- Browse pets by category (Dogs, Cats, Birds, etc.)
- Filter pets by breed/species
- Pet detail pages with full information
- Adoption application form with admin email notification
- Contact form with admin notification
- Responsive design (mobile + tablet + desktop)
- SEO-friendly meta tags and Open Graph support
- Django admin panel for managing content

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahmednabeen/PetCare.git
   cd PetCare
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   .\env\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the site** at `http://127.0.0.1:8000`

## Admin Panel

Navigate to `/admin/` and log in with your superuser credentials to manage:
- Categories and Pets
- Adoption Applications
- Contact Messages
- Site Settings
- Services and Content

## Email Configuration

Update `settings.py` with your SMTP credentials to enable admin notifications:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
ADMIN_EMAIL = 'admin@petcare.com'
```

Use a Gmail [App Password](https://support.google.com/accounts/answer/1858339) for security.

## Deployment

Before deploying to production, uncomment the production settings block in `settings.py` and set:

```python
DEBUG = False
ALLOWED_HOSTS = ['.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Tech Stack

- **Backend:** Django
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** HTML, CSS, JavaScript
