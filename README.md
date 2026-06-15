# Vatsalya Shree Hospital & HMS V1

A complete Django Hospital Website + Hospital Management System (HMS) built for Vatsalya Shree Hospital - Towards Better Child Health.

## Features

- **Public-facing website pages**:
  - Home Page with sliders, OPD timing lists, testimonial highlights, and interactive counters.
  - Detailed Doctor Profile of Dr. Kalpesh Patidar.
  - Interactive Gallery with lightbox image layout utilizing existing clinic images.
  - Services Overview (nicu care, child checkups, pediatric emergency).
  - Online Appointment Booking form with validations.
  - Contact page with database-connected inquiries.
  - FAQ list with common clinical and billing questions.
  - Privacy policy and terms & conditions templates.
  
- **HMS Dashboard (Staff Portal)**:
  - Total Patient Registry (Add/Edit/Delete/Search).
  - Appointment Booking Management (Filter by status, search by mobile, status updating).
  - Contact Message inbox control.
  - Gallery Uploader.
  - Service customizer list.
  - CSV export for appointment data.

## Installation & Setup

1. **Virtual Environment Setup**:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Dev Server**:
   ```bash
   python manage.py runserver
   ```
