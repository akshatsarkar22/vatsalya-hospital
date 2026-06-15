from django.urls import path
from . import views
from . import views_hms

urlpatterns = [
    # ── Public Pages ──────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('doctor/', views.doctor_profile, name='doctor'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment/success/<int:pk>/', views.appointment_success, name='appointment_success'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('testimonials/', views.testimonials_page, name='testimonials'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),

    # ── HMS - Dashboard ───────────────────────────────────────────────────────
    path('hms/', views_hms.hms_dashboard, name='hms_dashboard'),

    # ── HMS - Patients ────────────────────────────────────────────────────────
    path('hms/patients/', views_hms.patients_list, name='hms_patients'),
    path('hms/patients/add/', views_hms.patient_add, name='hms_patient_add'),
    path('hms/patients/edit/<int:pk>/', views_hms.patient_edit, name='hms_patient_edit'),
    path('hms/patients/delete/<int:pk>/', views_hms.patient_delete, name='hms_patient_delete'),
    path('hms/patients/<int:pk>/visits/', views_hms.patient_visits, name='hms_patient_visits'),
    path('hms/patients/<int:patient_pk>/visits/add/', views_hms.visit_add, name='hms_visit_add'),
    path('hms/visits/edit/<int:pk>/', views_hms.visit_edit, name='hms_visit_edit'),
    path('hms/visits/delete/<int:pk>/', views_hms.visit_delete, name='hms_visit_delete'),

    # ── HMS - Appointments ────────────────────────────────────────────────────
    path('hms/appointments/', views_hms.appointments_list, name='hms_appointments'),
    path('hms/appointments/add/', views_hms.appointment_add, name='hms_appointment_add'),
    path('hms/appointments/edit/<int:pk>/', views_hms.appointment_edit, name='hms_appointment_edit'),
    path('hms/appointments/delete/<int:pk>/', views_hms.appointment_delete, name='hms_appointment_delete'),
    path('hms/appointments/status/<int:pk>/<str:new_status>/', views_hms.appointment_status, name='hms_appointment_status'),

    # ── HMS - Contact Messages ─────────────────────────────────────────────────
    path('hms/messages/', views_hms.messages_list, name='hms_messages'),
    path('hms/messages/delete/<int:pk>/', views_hms.message_delete, name='hms_message_delete'),

    # ── HMS - Services ────────────────────────────────────────────────────────
    path('hms/services/', views_hms.services_list, name='hms_services'),
    path('hms/services/add/', views_hms.service_add, name='hms_service_add'),
    path('hms/services/edit/<int:pk>/', views_hms.service_edit, name='hms_service_edit'),
    path('hms/services/delete/<int:pk>/', views_hms.service_delete, name='hms_service_delete'),

    # ── HMS - Gallery ──────────────────────────────────────────────────────────
    path('hms/gallery/', views_hms.gallery_list, name='hms_gallery'),
    path('hms/gallery/upload/', views_hms.gallery_upload, name='hms_gallery_upload'),
    path('hms/gallery/delete/<int:pk>/', views_hms.gallery_delete, name='hms_gallery_delete'),

    # ── HMS - Testimonials ────────────────────────────────────────────────────
    path('hms/testimonials/', views_hms.testimonials_list, name='hms_testimonials'),
    path('hms/testimonials/add/', views_hms.testimonial_add, name='hms_testimonial_add'),
    path('hms/testimonials/edit/<int:pk>/', views_hms.testimonial_edit, name='hms_testimonial_edit'),
    path('hms/testimonials/delete/<int:pk>/', views_hms.testimonial_delete, name='hms_testimonial_delete'),

    # ── HMS - FAQs ────────────────────────────────────────────────────────────
    path('hms/faqs/', views_hms.faq_list, name='hms_faqs'),
    path('hms/faqs/add/', views_hms.faq_add, name='hms_faq_add'),
    path('hms/faqs/edit/<int:pk>/', views_hms.faq_edit, name='hms_faq_edit'),
    path('hms/faqs/delete/<int:pk>/', views_hms.faq_delete, name='hms_faq_delete'),

    # ── HMS - Settings ────────────────────────────────────────────────────────
    path('hms/settings/hospital/', views_hms.hospital_info_edit, name='hms_hospital_info'),
    path('hms/settings/doctor/', views_hms.doctor_profile_edit, name='hms_doctor_profile'),
]
