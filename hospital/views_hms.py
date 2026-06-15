import csv
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import staff_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from .models import (
    Patient, Appointment, ContactMessage, Service, GalleryImage,
    Testimonial, FAQ, HospitalInfo, DoctorProfile, VisitHistory
)
from .forms import (
    PatientForm, ServiceForm, GalleryImageForm, AppointmentForm,
    TestimonialForm, FAQForm, HospitalInfoForm, DoctorProfileForm, VisitHistoryForm
)


def get_hms_stats():
    today = timezone.now().date()
    return {
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'confirmed_appointments': Appointment.objects.filter(status='confirmed').count(),
        'cancelled_appointments': Appointment.objects.filter(status='cancelled').count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_services': Service.objects.count(),
        'total_gallery': GalleryImage.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_faqs': FAQ.objects.count(),
    }


# ─── Dashboard ────────────────────────────────────────────────────────────────

@staff_required
def hms_dashboard(request):
    stats = get_hms_stats()
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.filter(is_read=False)[:5]
    today_appointments = Appointment.objects.filter(
        appointment_date=timezone.now().date()
    ).order_by('appointment_time')

    return render(request, 'hms/dashboard.html', {
        'page_title': 'HMS Dashboard',
        'stats': stats,
        'recent_appointments': recent_appointments,
        'recent_messages': recent_messages,
        'today_appointments': today_appointments,
    })


# ─── Patient Management ───────────────────────────────────────────────────────

@staff_required
def patients_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(name__icontains=query) | Q(mobile__icontains=query)
        )

    paginator = Paginator(patients, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'hms/patients_list.html', {
        'page_title': 'Patient Directory',
        'patients': page_obj,
        'query': query,
        'stats': get_hms_stats(),
    })


@staff_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.name}" registered successfully!')
            return redirect('hms_patients')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PatientForm()

    return render(request, 'hms/patient_form.html', {
        'page_title': 'Register New Patient',
        'form': form,
        'action': 'Register',
    })


@staff_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient record "{patient.name}" updated successfully!')
            return redirect('hms_patients')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'hms/patient_form.html', {
        'page_title': 'Edit Patient Details',
        'form': form,
        'patient': patient,
        'action': 'Update',
    })


@staff_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.name
        patient.delete()
        messages.success(request, f'Patient "{name}" deleted successfully!')
    return redirect('hms_patients')


# ─── Visit History ────────────────────────────────────────────────────────────

@staff_required
def patient_visits(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    visits = patient.visits.all()
    return render(request, 'hms/patient_visits.html', {
        'page_title': f'Visit History – {patient.name}',
        'patient': patient,
        'visits': visits,
        'stats': get_hms_stats(),
    })


@staff_required
def visit_add(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = VisitHistoryForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            messages.success(request, f'Visit record added for "{patient.name}".')
            return redirect('hms_patient_visits', pk=patient.pk)
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = VisitHistoryForm()

    return render(request, 'hms/visit_form.html', {
        'page_title': f'Add Visit – {patient.name}',
        'form': form,
        'patient': patient,
        'action': 'Add',
    })


@staff_required
def visit_edit(request, pk):
    visit = get_object_or_404(VisitHistory, pk=pk)
    if request.method == 'POST':
        form = VisitHistoryForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visit record updated.')
            return redirect('hms_patient_visits', pk=visit.patient.pk)
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = VisitHistoryForm(instance=visit)

    return render(request, 'hms/visit_form.html', {
        'page_title': 'Edit Visit Record',
        'form': form,
        'patient': visit.patient,
        'visit': visit,
        'action': 'Update',
    })


@staff_required
def visit_delete(request, pk):
    visit = get_object_or_404(VisitHistory, pk=pk)
    patient_pk = visit.patient.pk
    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Visit record deleted.')
    return redirect('hms_patient_visits', pk=patient_pk)


# ─── Appointment Management ───────────────────────────────────────────────────

@staff_required
def appointments_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    appointments = Appointment.objects.all().order_by('-appointment_date', '-created_at')

    if query:
        appointments = appointments.filter(
            Q(child_name__icontains=query) |
            Q(parent_name__icontains=query) |
            Q(mobile__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)

    # CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="appointments_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Child Name', 'Parent Name', 'Mobile', 'Age',
                         'Date', 'Time', 'Reason', 'Status', 'Created At'])
        for appt in appointments:
            writer.writerow([
                appt.pk, appt.child_name, appt.parent_name, appt.mobile,
                appt.age, appt.appointment_date, appt.appointment_time,
                appt.reason, appt.get_status_display(),
                appt.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response

    paginator = Paginator(appointments, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Build WhatsApp number
    hospital = HospitalInfo.get_info()
    wa_number = hospital.whatsapp.replace('+', '').replace('-', '').replace(' ', '')

    return render(request, 'hms/appointments_list.html', {
        'page_title': 'Manage Appointments',
        'appointments': page_obj,
        'query': query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'stats': get_hms_stats(),
        'wa_number': wa_number,
    })


@staff_required
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            # Auto-register patient if not already exists
            Patient.objects.get_or_create(
                mobile=appt.mobile,
                defaults={
                    'name': appt.child_name,
                    'age': appt.age,
                    'address': 'Registered via Appointment Booking'
                }
            )
            messages.success(request, f'Appointment scheduled for "{appt.child_name}"!')
            return redirect('hms_appointments')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = AppointmentForm()

    return render(request, 'hms/appointment_form.html', {
        'page_title': 'Schedule Appointment',
        'form': form,
        'action': 'Create',
    })


@staff_required
def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            form.save()
            messages.success(request, f'Appointment updated for "{appt.child_name}".')
            return redirect('hms_appointments')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = AppointmentForm(instance=appt)

    return render(request, 'hms/appointment_form.html', {
        'page_title': 'Edit Appointment',
        'form': form,
        'appointment': appt,
        'action': 'Update',
    })


@staff_required
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        name = appt.child_name
        appt.delete()
        messages.success(request, f'Appointment record for "{name}" deleted.')
    return redirect('hms_appointments')


@staff_required
def appointment_status(request, pk, new_status):
    appt = get_object_or_404(Appointment, pk=pk)
    valid_statuses = ['pending', 'confirmed', 'cancelled']
    if new_status in valid_statuses:
        appt.status = new_status
        appt.save()
        messages.success(request, f'Appointment #{pk} status changed to {new_status.title()}.')
    else:
        messages.error(request, 'Invalid status update request.')
    return redirect('hms_appointments')


# ─── Contact Messages ─────────────────────────────────────────────────────────

@staff_required
def messages_list(request):
    msgs = ContactMessage.objects.all().order_by('-created_at')
    # Mark all as read on view
    ContactMessage.objects.filter(is_read=False).update(is_read=True)

    paginator = Paginator(msgs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'hms/messages_list.html', {
        'page_title': 'Inquiries Inbox',
        'messages_list': page_obj,
        'stats': get_hms_stats(),
    })


@staff_required
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('hms_messages')


# ─── Services Management ──────────────────────────────────────────────────────

@staff_required
def services_list(request):
    svc_list = Service.objects.all()
    return render(request, 'hms/services_list.html', {
        'page_title': 'Manage Clinic Services',
        'services': svc_list,
        'stats': get_hms_stats(),
    })


@staff_required
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            svc = form.save()
            messages.success(request, f'Service "{svc.title}" added successfully.')
            return redirect('hms_services')
        else:
            messages.error(request, 'Please resolve the errors.')
    else:
        form = ServiceForm()

    return render(request, 'hms/service_form.html', {
        'page_title': 'Add New Service',
        'form': form,
        'action': 'Add',
    })


@staff_required
def service_edit(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=svc)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{svc.title}" updated.')
            return redirect('hms_services')
        else:
            messages.error(request, 'Please resolve the errors.')
    else:
        form = ServiceForm(instance=svc)

    return render(request, 'hms/service_form.html', {
        'page_title': 'Edit Service',
        'form': form,
        'service': svc,
        'action': 'Update',
    })


@staff_required
def service_delete(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        title = svc.title
        svc.delete()
        messages.success(request, f'Service "{title}" deleted.')
    return redirect('hms_services')


# ─── Gallery Management ───────────────────────────────────────────────────────

@staff_required
def gallery_list(request):
    images = GalleryImage.objects.all()
    return render(request, 'hms/gallery_list.html', {
        'page_title': 'Photo Gallery',
        'images': images,
        'stats': get_hms_stats(),
    })


@staff_required
def gallery_upload(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            messages.success(request, f'Image "{img.title or "Gallery Image"}" uploaded.')
            return redirect('hms_gallery')
        else:
            messages.error(request, 'Failed to upload image.')
    else:
        form = GalleryImageForm()

    return render(request, 'hms/gallery_upload.html', {
        'page_title': 'Upload Gallery Image',
        'form': form,
    })


@staff_required
def gallery_delete(request, pk):
    img = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        if img.image:
            img.image.delete(save=False)
        img.delete()
        messages.success(request, 'Gallery image deleted.')
    return redirect('hms_gallery')


# ─── Testimonials Management ──────────────────────────────────────────────────

@staff_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'hms/testimonials_list.html', {
        'page_title': 'Manage Testimonials',
        'testimonials': testimonials,
        'stats': get_hms_stats(),
    })


@staff_required
def testimonial_add(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            t = form.save()
            messages.success(request, f'Testimonial by "{t.patient_name}" added.')
            return redirect('hms_testimonials')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = TestimonialForm()

    return render(request, 'hms/testimonial_form.html', {
        'page_title': 'Add Testimonial',
        'form': form,
        'action': 'Add',
    })


@staff_required
def testimonial_edit(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            messages.success(request, f'Testimonial updated.')
            return redirect('hms_testimonials')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = TestimonialForm(instance=t)

    return render(request, 'hms/testimonial_form.html', {
        'page_title': 'Edit Testimonial',
        'form': form,
        'testimonial': t,
        'action': 'Update',
    })


@staff_required
def testimonial_delete(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        name = t.patient_name
        t.delete()
        messages.success(request, f'Testimonial by "{name}" deleted.')
    return redirect('hms_testimonials')


# ─── FAQ Management ───────────────────────────────────────────────────────────

@staff_required
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'hms/faq_list.html', {
        'page_title': 'Manage FAQs',
        'faqs': faqs,
        'stats': get_hms_stats(),
    })


@staff_required
def faq_add(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save()
            messages.success(request, f'FAQ added successfully.')
            return redirect('hms_faqs')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = FAQForm()

    return render(request, 'hms/faq_form.html', {
        'page_title': 'Add FAQ',
        'form': form,
        'action': 'Add',
    })


@staff_required
def faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated.')
            return redirect('hms_faqs')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = FAQForm(instance=faq)

    return render(request, 'hms/faq_form.html', {
        'page_title': 'Edit FAQ',
        'form': form,
        'faq': faq,
        'action': 'Update',
    })


@staff_required
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ deleted.')
    return redirect('hms_faqs')


# ─── Hospital Info & Doctor Profile ──────────────────────────────────────────

@staff_required
def hospital_info_edit(request):
    info = HospitalInfo.get_info()
    if request.method == 'POST':
        form = HospitalInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hospital information updated successfully.')
            return redirect('hms_hospital_info')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = HospitalInfoForm(instance=info)

    return render(request, 'hms/hospital_info_form.html', {
        'page_title': 'Hospital Information',
        'form': form,
        'info': info,
    })


@staff_required
def doctor_profile_edit(request):
    profile = DoctorProfile.get_profile()
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor profile updated successfully.')
            return redirect('hms_doctor_profile')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = DoctorProfileForm(instance=profile)

    return render(request, 'hms/doctor_profile_form.html', {
        'page_title': 'Doctor Profile',
        'form': form,
        'profile': profile,
    })
