from django.contrib import admin
from .models import Doctor, Patient, Appointment, ContactMessage, Service, GalleryImage, Testimonial


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'qualification', 'specialization', 'experience', 'consultation_fee']
    search_fields = ['name', 'specialization']
    list_filter = ['specialization']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'age', 'created_at']
    search_fields = ['name', 'mobile']
    list_filter = ['created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'parent_name', 'mobile', 'appointment_date',
                    'appointment_time', 'status', 'created_at']
    search_fields = ['child_name', 'parent_name', 'mobile']
    list_filter = ['status', 'appointment_date']
    ordering = ['-appointment_date']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'appointment_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['is_read', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    list_editable = ['is_read']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    search_fields = ['title']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    search_fields = ['title', 'category']
    list_filter = ['category', 'uploaded_at']
    ordering = ['-uploaded_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'rating', 'is_active', 'created_at']
    search_fields = ['patient_name']
    list_filter = ['rating', 'is_active']
    list_editable = ['is_active']
    ordering = ['-created_at']


# Customize admin site headers
admin.site.site_header = 'Vatsalya Shree Hospital Admin'
admin.site.site_title = 'VSH Admin Portal'
admin.site.index_title = 'Hospital Management'
