from django.contrib import admin
from .models import (
    HospitalInfo, DoctorProfile, Patient, Appointment,
    ContactMessage, Service, GalleryImage, Testimonial, FAQ, VisitHistory
)


@admin.register(HospitalInfo)
class HospitalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'email', 'working_days', 'updated_at']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Allow only one HospitalInfo record
        if self.model.objects.count() >= 1:
            return False
        return True


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'qualification', 'specialization', 'experience', 'consultation_fee']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Allow only one DoctorProfile record
        if self.model.objects.count() >= 1:
            return False
        return True


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'age', 'created_at']
    search_fields = ['name', 'mobile']
    list_filter = ['created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(VisitHistory)
class VisitHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit_date', 'diagnosis', 'weight', 'created_at']
    search_fields = ['patient__name', 'diagnosis']
    list_filter = ['visit_date', 'created_at']
    ordering = ['-visit_date']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'child_name', 'parent_name', 'mobile', 'appointment_date',
        'appointment_time', 'status', 'created_at'
    ]
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


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


# Customize admin site headers
admin.site.site_header = 'Vatsalya Shree Hospital — Admin'
admin.site.site_title = 'VSH Admin Portal'
admin.site.index_title = 'Hospital Management'
