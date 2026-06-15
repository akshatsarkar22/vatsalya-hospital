import csv
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.utils import timezone

from .models import Doctor, Service, GalleryImage, Testimonial, Appointment
from .forms import AppointmentForm, ContactForm

# ─── Context helpers ──────────────────────────────────────────────────────────

HOSPITAL_INFO = {
    'name': 'Vatsalya Shree Hospital',
    'tagline': 'Towards Better Child Health',
    'address': 'A.B. Road, Guljhara, Dhamnod, Madhya Pradesh',
    'mobile': '+91-XXXXXXXXXX', # Developer placeholder to be customized
    'whatsapp': '+91-XXXXXXXXXX',
    'email': 'info@vatsalyashreehospital.com',
    'reg_no': 'NH/7245/MAY-2026',
    'opd_morning': '10:00 AM – 2:00 PM',
    'opd_evening': '5:00 PM – 8:00 PM',
    'working_days': 'Tuesday to Sunday',
    'holiday': 'Monday',
}

DOCTOR_INFO = {
    'name': 'Dr. Kalpesh Patidar',
    'qualification': 'M.B.B.S. (Nagpur), M.D. (Gwalior)',
    'specialization': "Children's and New Born Disease Specialist",
    'experience': 12,
    'consultation_fee': 350,
}

DEFAULT_SERVICES = [
    {'title': 'Child Specialist Consultation', 'icon': 'bi-person-heart', 'description': 'Expert pediatric consultations for all childhood ailments with personalized care.'},
    {'title': 'New Born Care', 'icon': 'bi-emoji-smile', 'description': 'Specialized care for newborns including health monitoring and feeding guidance.'},
    {'title': 'Vaccination', 'icon': 'bi-capsule', 'description': 'Complete vaccination schedule for children as per national immunization program.'},
    {'title': 'NICU Care', 'icon': 'bi-hospital', 'description': 'Advanced Neonatal Intensive Care Unit for premature and critically ill newborns.'},
    {'title': 'Growth Monitoring', 'icon': 'bi-graph-up-arrow', 'description': 'Regular tracking of child\'s height, weight and developmental milestones.'},
    {'title': 'Pediatric Emergency', 'icon': 'bi-heart-pulse', 'description': '24/7 emergency care for children with experienced medical staff on standby.'},
    {'title': 'Child Health Checkups', 'icon': 'bi-clipboard2-pulse', 'description': 'Comprehensive health checkup packages designed specifically for children.'},
    {'title': 'General Pediatric Services', 'icon': 'bi-bandaid', 'description': 'Wide range of general pediatric services covering all aspects of child health.'},
]

DEFAULT_TESTIMONIALS = [
    {'patient_name': 'Sunita Sharma', 'feedback': 'Dr. Kalpesh is an excellent doctor. He diagnosed my son\'s illness very quickly and the treatment was effective. Highly recommended!', 'rating': 5},
    {'patient_name': 'Ramesh Patel', 'feedback': 'Very professional and caring staff. The hospital is clean and well-maintained. My daughter received the best care here.', 'rating': 5},
    {'patient_name': 'Priya Verma', 'feedback': 'I am grateful to Dr. Kalpesh and his team for saving my newborn. The NICU care was exceptional. God bless this hospital!', 'rating': 5},
    {'patient_name': 'Anil Malviya', 'feedback': 'Excellent pediatric care. Doctor explains everything clearly and takes time with each patient. Very satisfied with the treatment.', 'rating': 4},
    {'patient_name': 'Kavita Joshi', 'feedback': 'The best children\'s hospital in the region. Dr. Patidar is very knowledgeable and the staff is very cooperative.', 'rating': 5},
]

FAQ_LIST = [
    {'q': 'What are the OPD timings?', 'a': 'OPD is available Morning: 10:00 AM – 2:00 PM and Evening: 5:00 PM – 8:00 PM, Tuesday to Sunday.'},
    {'q': 'Is Monday a weekly holiday?', 'a': 'Yes, Vatsalya Shree Hospital is closed on Mondays.'},
    {'q': 'What is the consultation fee?', 'a': 'The consultation fee is ₹350 per visit.'},
    {'q': 'Does the hospital have NICU facilities?', 'a': 'Yes, we have an advanced Neonatal Intensive Care Unit (NICU) for premature and critically ill infants.'},
    {'q': 'Can I book an appointment online?', 'a': 'Yes, you can schedule and book appointments online through our appointment system.'},
    {'q': 'What is the age limit for patients?', 'a': 'Dr. Kalpesh Patidar specializes in children from newborn stage up to 18 years of age.'},
    {'q': 'What vaccinations are available?', 'a': 'We provide all national and custom pediatric vaccinations (BCG, Polio, DPT, MMR, Typhoid, etc.) during OPD hours.'},
    {'q': 'Where is the clinic located?', 'a': 'We are located at A.B. Road, Guljhara, Dhamnod, Madhya Pradesh.'},
]


def get_base_context():
    return {
        'hospital': HOSPITAL_INFO,
        'doctor': DOCTOR_INFO,
    }


# ─── Public Views ──────────────────────────────────────────────────────────────

def home(request):
    services = Service.objects.filter(is_active=True)[:8]
    if not services.exists():
        services = DEFAULT_SERVICES

    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    if not testimonials.exists():
        testimonials = DEFAULT_TESTIMONIALS

    gallery_images = GalleryImage.objects.all()[:6]

    stats = {
        'patients': Appointment.objects.values('mobile').distinct().count() or 500,
        'experience': 12,
        'services': 8,
        'rating': 5,
    }

    context = get_base_context()
    context.update({
        'page_title': 'Home',
        'services': services,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'stats': stats,
        'hero_images': [
            'images/hospital-1.jpeg',
            'images/hospital-2.jpeg',
            'images/hospital-3.jpeg',
        ],
    })
    return render(request, 'hospital/home.html', context)


def about(request):
    context = get_base_context()
    context.update({
        'page_title': 'About Hospital',
        'about_images': [
            'images/hospital-4.jpeg',
            'images/hospital-5.jpeg',
        ],
    })
    return render(request, 'hospital/about.html', context)


def doctor_profile(request):
    try:
        doctor = Doctor.objects.first()
    except Doctor.DoesNotExist:
        doctor = None

    context = get_base_context()
    context.update({
        'page_title': 'Doctor Profile',
        'db_doctor': doctor,
    })
    return render(request, 'hospital/doctor.html', context)


def services(request):
    db_services = Service.objects.filter(is_active=True)

    context = get_base_context()
    context.update({
        'page_title': 'Our Services',
        'services': db_services if db_services.exists() else DEFAULT_SERVICES,
    })
    return render(request, 'hospital/services.html', context)


def gallery(request):
    gallery_images = GalleryImage.objects.all()
    categories = GalleryImage.objects.values_list('category', flat=True).distinct()

    # Static images fallback
    static_images = [
        {'src': 'images/hospital-1.jpeg', 'title': 'Hospital Entrance', 'category': 'Hospital'},
        {'src': 'images/hospital-2.jpeg', 'title': 'OPD Area', 'category': 'OPD'},
        {'src': 'images/hospital-3.jpeg', 'title': 'Patient Ward', 'category': 'Wards'},
        {'src': 'images/hospital-4.jpeg', 'title': 'NICU Unit', 'category': 'NICU'},
        {'src': 'images/hospital-5.jpeg', 'title': 'Emergency Care', 'category': 'Emergency'},
        {'src': 'images/hospital-6.jpeg', 'title': 'Consultation Room', 'category': 'OPD'},
        {'src': 'images/hospital-7.jpeg', 'title': 'Laboratory', 'category': 'Hospital'},
        {'src': 'images/hospital-8.jpeg', 'title': 'Reception', 'category': 'Hospital'},
    ]

    context = get_base_context()
    context.update({
        'page_title': 'Gallery',
        'gallery_images': gallery_images,
        'categories': categories,
        'static_images': static_images,
    })
    return render(request, 'hospital/gallery.html', context)


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            messages.success(request, f'Appointment booked successfully! Your booking ID is #{appt.pk}. We will contact you soon.')
            return redirect('appointment_success', pk=appt.pk)
        else:
            messages.error(request, 'Please correct the errors in the booking form.')
    else:
        form = AppointmentForm()

    context = get_base_context()
    context.update({
        'page_title': 'Book Appointment',
        'form': form,
        'today': date.today().isoformat(),
    })
    return render(request, 'hospital/appointment.html', context)


def appointment_success(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    context = get_base_context()
    context.update({
        'page_title': 'Booking Successful',
        'appointment': appt,
    })
    return render(request, 'hospital/appointment_success.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully. We will get back to you shortly.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = get_base_context()
    context.update({
        'page_title': 'Contact Us',
        'form': form,
    })
    return render(request, 'hospital/contact.html', context)


def faq(request):
    context = get_base_context()
    context.update({
        'page_title': 'FAQ',
        'faqs': FAQ_LIST,
    })
    return render(request, 'hospital/faq.html', context)


def privacy_policy(request):
    context = get_base_context()
    context['page_title'] = 'Privacy Policy'
    return render(request, 'hospital/privacy.html', context)


def terms_conditions(request):
    context = get_base_context()
    context['page_title'] = 'Terms & Conditions'
    return render(request, 'hospital/terms.html', context)


def custom_404(request, exception=None):
    context = get_base_context()
    context['page_title'] = '404 - Page Not Found'
    return render(request, '404.html', context, status=404)
