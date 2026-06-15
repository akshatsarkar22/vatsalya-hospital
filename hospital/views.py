import csv
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import (
    HospitalInfo, DoctorProfile, Service, GalleryImage,
    Testimonial, Appointment, FAQ
)
from .forms import AppointmentForm, ContactForm, UserRegistrationForm, CustomLoginForm


# ─── Context helpers ──────────────────────────────────────────────────────────

DEFAULT_SERVICES = [
    {'title': 'Child Specialist Consultation', 'icon': 'bi-person-heart',
     'description': 'Expert pediatric consultations for all childhood ailments with personalized care.'},
    {'title': 'New Born Care', 'icon': 'bi-emoji-smile',
     'description': 'Specialized care for newborns including health monitoring and feeding guidance.'},
    {'title': 'Vaccination', 'icon': 'bi-capsule',
     'description': 'Complete vaccination schedule for children as per national immunization program.'},
    {'title': 'NICU Care', 'icon': 'bi-hospital',
     'description': 'Advanced Neonatal Intensive Care Unit for premature and critically ill newborns.'},
    {'title': 'Growth Monitoring', 'icon': 'bi-graph-up-arrow',
     'description': 'Regular tracking of child\'s height, weight and developmental milestones.'},
    {'title': 'Pediatric Emergency', 'icon': 'bi-heart-pulse',
     'description': '24/7 emergency care for children with experienced medical staff on standby.'},
    {'title': 'Child Health Checkups', 'icon': 'bi-clipboard2-pulse',
     'description': 'Comprehensive health checkup packages designed specifically for children.'},
    {'title': 'General Pediatric Services', 'icon': 'bi-bandaid',
     'description': 'Wide range of general pediatric services covering all aspects of child health.'},
]

DEFAULT_TESTIMONIALS = [
    {'patient_name': 'Sunita Sharma', 'rating': 5,
     'feedback': 'Dr. Kalpesh is an excellent doctor. He diagnosed my son\'s illness very quickly and the treatment was effective. Highly recommended!'},
    {'patient_name': 'Ramesh Patel', 'rating': 5,
     'feedback': 'Very professional and caring staff. The hospital is clean and well-maintained. My daughter received the best care here.'},
    {'patient_name': 'Priya Verma', 'rating': 5,
     'feedback': 'I am grateful to Dr. Kalpesh and his team for saving my newborn. The NICU care was exceptional. God bless this hospital!'},
    {'patient_name': 'Anil Malviya', 'rating': 4,
     'feedback': 'Excellent pediatric care. Doctor explains everything clearly and takes time with each patient. Very satisfied with the treatment.'},
    {'patient_name': 'Kavita Joshi', 'rating': 5,
     'feedback': 'The best children\'s hospital in the region. Dr. Patidar is very knowledgeable and the staff is very cooperative.'},
]

DEFAULT_FAQS = [
    {'question': 'What are the OPD timings?',
     'answer': 'OPD is available Morning: 10:00 AM – 2:00 PM and Evening: 5:00 PM – 8:00 PM, Tuesday to Sunday.'},
    {'question': 'Is Monday a weekly holiday?',
     'answer': 'Yes, Vatsalya Shree Hospital is closed on Mondays.'},
    {'question': 'What is the consultation fee?',
     'answer': 'The consultation fee is ₹350 per visit.'},
    {'question': 'Does the hospital have NICU facilities?',
     'answer': 'Yes, we have an advanced Neonatal Intensive Care Unit (NICU) for premature and critically ill infants.'},
    {'question': 'Can I book an appointment online?',
     'answer': 'Yes, you can schedule and book appointments online through our appointment system.'},
    {'question': 'What is the age limit for patients?',
     'answer': 'Dr. Kalpesh Patidar specializes in children from newborn stage up to 18 years of age.'},
    {'question': 'What vaccinations are available?',
     'answer': 'We provide all national and custom pediatric vaccinations (BCG, Polio, DPT, MMR, Typhoid, etc.) during OPD hours.'},
    {'question': 'Where is the clinic located?',
     'answer': 'We are located at A.B. Road, Guljhara, Dhamnod, Madhya Pradesh.'},
]


def get_base_context():
    hospital = HospitalInfo.get_info()
    doctor = DoctorProfile.get_profile()
    return {
        'hospital': hospital,
        'doctor': doctor,
    }


def _is_staff_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_post_login_redirect(user, next_url=None):
    if _is_staff_user(user):
        if next_url and next_url.startswith('/') and not next_url.startswith('/register'):
            return next_url
        return reverse('hms_dashboard')

    if next_url and next_url.startswith('/') and not next_url.startswith('/hms') and not next_url.startswith('/register'):
        return next_url
    return reverse('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect(get_post_login_redirect(request.user))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully. Please log in with your credentials.',
            )
            return redirect('login')
        messages.error(request, 'Please correct the errors below to complete registration.')
    else:
        form = UserRegistrationForm()

    context = get_base_context()
    context.update({
        'page_title': 'Register',
        'form': form,
    })
    return render(request, 'hospital/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_post_login_redirect(request.user))

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(get_post_login_redirect(user, next_url))
        messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = CustomLoginForm()

    context = get_base_context()
    context.update({
        'page_title': 'Login',
        'form': form,
        'next': next_url or '',
    })
    return render(request, 'hospital/login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ─── Public Views ──────────────────────────────────────────────────────────────

def home(request):
    services = Service.objects.filter(is_active=True)[:8]
    if not services.exists():
        services = DEFAULT_SERVICES

    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    if not testimonials.exists():
        testimonials = DEFAULT_TESTIMONIALS

    gallery_images = GalleryImage.objects.all()[:6]

    stats = {
        'patients': Appointment.objects.values('mobile').distinct().count() or 500,
        'experience': DoctorProfile.get_profile().experience,
        'services': Service.objects.filter(is_active=True).count() or 8,
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
    doctor = DoctorProfile.get_profile()
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

    # Static fallback images
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
            messages.success(
                request,
                f'Appointment booked successfully! Your Booking ID is #{appt.pk}. '
                f'We will contact you soon to confirm.'
            )
            return redirect('appointment_success', pk=appt.pk)
        else:
            messages.error(request, 'Please correct the errors in the booking form.')
    else:
        initial = {}
        if request.user.is_authenticated and not _is_staff_user(request.user):
            initial['parent_name'] = request.user.get_full_name() or request.user.username
            profile = getattr(request.user, 'profile', None)
            if profile and profile.phone:
                initial['mobile'] = profile.phone
        form = AppointmentForm(initial=initial)

    context = get_base_context()
    context.update({
        'page_title': 'Book Appointment',
        'form': form,
        'today': date.today().isoformat(),
    })
    return render(request, 'hospital/appointment.html', context)


def appointment_success(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    hospital = HospitalInfo.get_info()
    whatsapp_number = hospital.whatsapp.replace('+', '').replace('-', '').replace(' ', '')
    whatsapp_msg = (
        f"Hello! I have booked an appointment at Vatsalya Shree Hospital.%0A"
        f"Booking ID: %23{appt.pk}%0A"
        f"Child Name: {appt.child_name}%0A"
        f"Date: {appt.appointment_date}%0A"
        f"Time: {appt.appointment_time}%0A"
        f"Please confirm my appointment. Thank you!"
    )
    context = get_base_context()
    context.update({
        'page_title': 'Booking Successful',
        'appointment': appt,
        'whatsapp_number': whatsapp_number,
        'whatsapp_msg': whatsapp_msg,
    })
    return render(request, 'hospital/appointment_success.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you! Your message has been sent successfully. We will get back to you shortly.'
            )
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
    db_faqs = FAQ.objects.filter(is_active=True)
    context = get_base_context()
    context.update({
        'page_title': 'Frequently Asked Questions',
        'faqs': db_faqs if db_faqs.exists() else DEFAULT_FAQS,
    })
    return render(request, 'hospital/faq.html', context)


def testimonials_page(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    if not testimonials.exists():
        testimonials = DEFAULT_TESTIMONIALS
    context = get_base_context()
    context.update({
        'page_title': 'Patient Testimonials',
        'testimonials': testimonials,
    })
    return render(request, 'hospital/testimonials.html', context)


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
    context['page_title'] = '404 – Page Not Found'
    return render(request, '404.html', context, status=404)
