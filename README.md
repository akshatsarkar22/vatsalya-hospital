# Vatsalya Shree Hospital — Django HMS

A complete, production-ready **Hospital Management System (HMS)** and **Public Website** built with Django 5.2 for **Vatsalya Shree Hospital**, Dhamnod, Madhya Pradesh.

**Doctor:** Dr. Kalpesh Manager (Patidar) | M.B.B.S, MD | Children & New Born Specialist

---

## 🚀 Quick Setup

### 1. Clone / Extract Project
```bash
cd "New Hospital"
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / Mac
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Staff Login)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit → `http://127.0.0.1:8000/`

---

## 🌐 Public Pages

| Page | URL |
|------|-----|
| Home | `/` |
| About | `/about/` |
| Doctor Profile | `/doctor/` |
| Services | `/services/` |
| Gallery | `/gallery/` |
| Book Appointment | `/appointment/` |
| Appointment Success | `/appointment/success/<pk>/` |
| Contact Us | `/contact/` |
| FAQ | `/faq/` |
| Testimonials | `/testimonials/` |
| Privacy Policy | `/privacy-policy/` |
| Terms & Conditions | `/terms-conditions/` |

---

## 🏥 Staff Dashboard (HMS)

**Login:** `/admin/login/` (Django admin credentials)

| Feature | URL |
|---------|-----|
| Dashboard Overview | `/hms/` |
| Patients Directory | `/hms/patients/` |
| Patient Visit History | `/hms/patients/<pk>/visits/` |
| Appointments (CRUD + Export CSV) | `/hms/appointments/` |
| Contact Messages Inbox | `/hms/messages/` |
| Services Management | `/hms/services/` |
| Gallery Management | `/hms/gallery/` |
| Testimonials Management | `/hms/testimonials/` |
| FAQ Management | `/hms/faqs/` |
| Hospital Info Settings | `/hms/settings/hospital/` |
| Doctor Profile Settings | `/hms/settings/doctor/` |

---

## ✨ Key Features

- **Single staff/admin login** via Django auth
- **Dynamic content** from database (HospitalInfo, DoctorProfile singletons)
- **Appointment booking** with:
  - Past date prevention
  - Duplicate slot detection
  - WhatsApp confirm button on success page
- **Patient visit history** with prescription notes
- **Appointment CSV export** with search/filter
- **WhatsApp confirm button** in appointments list
- **Floating WhatsApp** widget on all public pages
- **Messages framework** alerts
- **Pagination** on all list views
- **Fully mobile responsive** Bootstrap 5 design
- **Loading screen** animation
- **Hero slider** with static images

---

## 📁 Project Structure

```
New Hospital/
├── hospital/               # Main app
│   ├── models.py           # All 10 models
│   ├── views.py            # Public page views
│   ├── views_hms.py        # Dashboard views
│   ├── forms.py            # All forms with validation
│   ├── admin.py            # Admin registrations
│   └── urls.py             # URL patterns
├── templates/
│   ├── base.html           # Public base template
│   ├── hospital/           # Public page templates
│   └── hms/                # Dashboard templates
├── static/
│   ├── css/style.css       # Custom styles
│   ├── js/main.js          # JavaScript
│   └── images/             # Hospital images
├── media/                  # Uploaded files
├── vatsalya_hospital/      # Project settings
├── manage.py
└── requirements.txt
```

---

## 🔐 Staff Login

Visit `/admin/login/` with the superuser credentials created during setup.  
All HMS routes (`/hms/*`) require staff login automatically.

---

## 📞 Hospital Contact

- **Address:** A.B. Road, Guljhara, Dhamnod, Madhya Pradesh
- **OPD:** Morning 10AM–2PM | Evening 5PM–8PM
- **Days:** Tuesday to Sunday (Monday: Closed)
- **Consultation Fee:** ₹350

---

*Built with ❤️ using Django 5.2, Bootstrap 5, SQLite*
