<<<<<<< HEAD
# TAS — Travel Agency System (Prototype)

This repository contains a modular Django project scaffold for an online travel management system (flights, hotels, packages, bookings, payments, admin dashboard, and REST APIs).

Quick start

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env
# adjust .env values
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_data.json  # optional
python manage.py runserver
```

Seed sample data:

```bash
python manage.py seed
```

Notes
- Uses Django REST Framework + Simple JWT for API auth.
- Tailwind integration and UI polish are left as next steps (use CDN or django-tailwind).
- Database defaults to sqlite; set Postgres env vars to use Postgres in production.
=======
# TAS-travel
>>>>>>> 2bf88bb2016351c00b116513835196fc54b365e0
