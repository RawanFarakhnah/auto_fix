# Auto Fix 🚗🔧

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.0%2B-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A Django-based web platform that helps car owners manage their vehicles, find nearby workshops, diagnose car issues using AI, set maintenance reminders, and leave service reviews.

---

## ✨ Features

- **📍 Find Nearest Workshop:** Locate workshops using geolocation or address-based proximity.
- **🧠 AI Car Diagnosis:** Chat with an AI assistant to identify potential issues based on symptoms.
- **⭐ Service Reviews:** Rate and review workshops and services.
- **⏰ Maintenance Notifications:** Get reminded about periodic car maintenance.
- **🔐 Authentication:** Secure login and user management.
- **📱 Responsive UI:** Mobile-friendly and intuitive design.
- **🔄 Dynamic Content:** AJAX-powered interactions.
- **🗂️ Relational DB:** MySQL with Django ORM.
- **🌐 REST API:** Easily integrate with mobile or third-party services.

---

## 🙌 Special Thanks

We extend our deepest gratitude to **Axsos Academy** for providing a transformative learning journey.  
A heartfelt thank you to our **instructor** and **teaching assistant** for their continuous guidance, encouragement, and knowledge-sharing throughout this project.  
This platform is a testament to the power of learning through collaboration.

### 👩‍💻 Team Members
- [Rawan Farakhna](https://www.linkedin.com/in/rawanfarakhna/)
- [Mujahed Qasem](https://www.linkedin.com/in/mujahed-qasem/)
- [Yasmeena Bassam](https://www.linkedin.com/in/yasmeena-bassam-yousef-a8b4b1346/)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/RawanFarakhnah/auto-fix.git
cd auto-fix

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE auto_fix_db;
```

2. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auto_fix_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### Run Application
```bash
# Apply database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📂 Project Structure

```
auto_fix/
├── accounts/
│   ├── models.py
│   ├── views.py
├── admin_dashboard/
│   ├── models.py
│   ├── views.py
├── ai_diagnosis/
│   ├── models.py
│   ├── views.py
├── auto_fix/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── bookings/
│   ├── models.py
│   ├── views.py
├── cars/
│   ├── models.py
│   ├── views.py
├── landing/
│   ├── models.py
│   ├── views.py
├── locations/
│   ├── models.py
│   ├── views.py
├── media/
│   ├── workshops_images/
├── owner_dashboard/
│   ├── models.py
│   ├── views.py
├── reviews/
│   ├── models.py
│   ├── views.py
├── user_dashboard/
│   ├── models.py
│   ├── views.py
├── workshops/
│   ├── models.py
│   ├── views.py
├── templates/
│   ├── base.html
│   ├── base2.html
│   ├── accounts/
│   ├── admin_dashboard/
│   ├── landing/
│   ├── owner_dashboard/
│   └── user_dashboard/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── manage.py
├── requirements.txt
├── README.md
```
---

## 🔒 Security Features

- ✅ CSRF protection  
- ✅ Password hashing  
- ✅ Secure user authentication  
- ✅ Role-based access control  
- ✅ Rate limiting for sensitive endpoints  

---

## 🛠️ Tech Stack

- **Backend:** Django 4.0+
- **Database:** MySQL 8.0+
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Django Allauth
- **AI Logic:** Custom Python AI models (extendable)

---
