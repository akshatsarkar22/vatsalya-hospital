import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, Count
from django.utils import timezone

from .models import Patient, Appointment, ContactMessage, Service, GalleryImage, Testimonial
from .forms import PatientForm, ServiceForm, GalleryImageForm, AppointmentForm


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
    }


# ─── Dashboard ────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
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

@staff_member_required(login_url='/admin/login/')
def patients_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(name__icontains=query) | Q(mobile__icontains=query)
        )

    return render(request, 'hms/patients_list.html', {
        'page_title': 'Patient Directory',
        'patients': patients,
        'query': query,
        'stats': get_hms_stats(),
    })


@staff_member_required(login_url='/admin/login/')
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


@staff_member_required(login_url='/admin/login/')
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


@staff_member_required(login_url='/admin/login/')
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.name
        patient.delete()
        messages.success(request, f'Patient "{name}" deleted successfully!')
    return redirect('hms_patients')


# ─── Appointment Management ───────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
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
                appt.reason, appt.get_status_display(), appt.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response

    return render(request, 'hms/appointments_list.html', {
        'page_title': 'Manage Appointments',
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'stats': get_hms_stats(),
    })


@staff_member_required(login_url='/admin/login/')
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            # Also register as patient if not already exists
            Patient.objects.get_or_create(
                mobile=appt.mobile,
                defaults={
                    'name': appt.child_name,
                    'age': appt.age,
                    'address': 'Registered via Appointment Booking'
                }
            )
            messages.success(request, f'Appointment scheduled successfully for "{appt.child_name}"!')
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


@staff_member_required(login_url='/admin/login/')
def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            form.save()
            messages.success(request, f'Appointment details updated for "{appt.child_name}".')
            return redirect('hms_appointments')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = AppointmentForm(instance=appt)

    return render(request, 'hms/appointment_form.html', {
        'page_title': 'Edit Appointment Schedule',
        'form': form,
        'appointment': appt,
        'action': 'Update',
    })


@staff_member_required(login_url='/admin/login/')
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        name = appt.child_name
        appt.delete()
        messages.success(request, f'Appointment record for "{name}" has been deleted.')
    return redirect('hms_appointments')


@staff_member_required(login_url='/admin/login/')
def appointment_status(request, pk, new_status):
    appt = get_object_or_404(Appointment, pk=pk)
    valid_statuses = ['pending', 'confirmed', 'cancelled']
    if new_status in valid_statuses:
        appt.status = new_status
        appt.save()
        messages.success(request, f'Appointment status changed to {new_status.title()}.')
    else:
        messages.error(request, 'Invalid status update request.')
    return redirect('hms_appointments')


# ─── Contact Messages ─────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def messages_list(request):
    msgs = ContactMessage.objects.all().order_by('-created_at')
    # Automatically mark all loaded messages as read
    ContactMessage.objects.filter(is_read=False).update(is_read=True)

    return render(request, 'hms/messages_list.html', {
        'page_title': 'Inquiries Inbox',
        'messages_list': msgs,
        'stats': get_hms_stats(),
    })


@staff_member_required(login_url='/admin/login/')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('hms_messages')


# ─── Services Management ──────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def services_list(request):
    services = Service.objects.all()
    return render(request, 'hms/services_list.html', {
        'page_title': 'Manage Clinic Services',
        'services': services,
        'stats': get_hms_stats(),
    })


@staff_member_required(login_url='/admin/login/')
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            svc = form.save()
            messages.success(request, f'Service "{svc.title}" successfully added.')
            return redirect('hms_services')
        else:
            messages.error(request, 'Please resolve the errors.')
    else:
        form = ServiceForm()

    return render(request, 'hms/service_form.html', {
        'page_title': 'Add New Clinic Service',
        'form': form,
        'action': 'Add',
    })


@staff_member_required(login_url='/admin/login/')
def service_edit(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=svc)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service details for "{svc.title}" updated.')
            return redirect('hms_services')
        else:
            messages.error(request, 'Please resolve the errors.')
    else:
        form = ServiceForm(instance=svc)

    return render(request, 'hms/service_form.html', {
        'page_title': 'Edit Service Details',
        'form': form,
        'service': svc,
        'action': 'Update',
    })


@staff_member_required(login_url='/admin/login/')
def service_delete(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        title = svc.title
        svc.delete()
        messages.success(request, f'Service "{title}" deleted.')
    return redirect('hms_services')


# ─── Gallery Management ───────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def gallery_list(request):
    images = GalleryImage.objects.all()
    return render(request, 'hms/gallery_list.html', {
        'page_title': 'Clinic Photo Gallery',
        'images': images,
        'stats': get_hms_stats(),
    })


@staff_member_required(login_url='/admin/login/')
def gallery_upload(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            messages.success(request, f'Image "{img.title or "Gallery Image"}" successfully uploaded.')
            return redirect('hms_gallery')
        else:
            messages.error(request, 'Failed to upload image. Please check the inputs.')
    else:
        form = GalleryImageForm()

    return render(request, 'hms/gallery_upload.html', {
        'page_title': 'Upload Image to Gallery',
        'form': form,
    })


@staff_member_required(login_url='/admin/login/')
def gallery_delete(request, pk):
    img = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        # Safely delete image file from storage if it exists
        if img.image:
            img.image.delete(save=False)
        img.delete()
        messages.success(request, 'Gallery image deleted.')
    return redirect('hms_gallery')
