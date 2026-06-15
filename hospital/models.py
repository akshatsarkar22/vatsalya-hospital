from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    """Optional profile data for registered public users."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user.username} profile'


class HospitalInfo(models.Model):
    """Singleton model for hospital contact & operational info."""
    name = models.CharField(max_length=200, default='Vatsalya Shree Hospital')
    tagline = models.CharField(max_length=300, default='Towards Better Child Health')
    address = models.TextField(default='A.B. Road, Guljhara, Dhamnod, Madhya Pradesh')
    mobile = models.CharField(max_length=20, default='+91-XXXXXXXXXX')
    whatsapp = models.CharField(max_length=20, default='+91-XXXXXXXXXX')
    email = models.EmailField(default='info@vatsalyashreehospital.com')
    reg_no = models.CharField(max_length=100, default='NH/7245/MAY-2026')
    opd_morning = models.CharField(max_length=100, default='10:00 AM – 2:00 PM')
    opd_evening = models.CharField(max_length=100, default='5:00 PM – 8:00 PM')
    working_days = models.CharField(max_length=200, default='Tuesday to Sunday')
    holiday = models.CharField(max_length=100, default='Monday')
    map_embed_url = models.URLField(
        blank=True,
        default='',
        help_text='Google Maps embed URL (iframe src)'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hospital Info'
        verbose_name_plural = 'Hospital Info'

    def __str__(self):
        return self.name

    @classmethod
    def get_info(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class DoctorProfile(models.Model):
    """Singleton model for the single doctor profile."""
    name = models.CharField(max_length=200, default='Dr. Kalpesh Manager (Patidar)')
    qualification = models.CharField(max_length=400, default='M.B.B.S, MD')
    specialization = models.CharField(
        max_length=300,
        default='Children & New Born Specialist'
    )
    experience = models.IntegerField(default=12, help_text='Years of experience')
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=350.00)
    image = models.ImageField(upload_to='doctor/', blank=True, null=True)
    about = models.TextField(
        blank=True,
        default='Dr. Kalpesh Patidar is a dedicated Children and Newborn Disease '
                'Specialist with over 12 years of experience in pediatric medicine. '
                'His compassionate approach and expertise have made Vatsalya Shree '
                'Hospital a trusted name for child healthcare in Dhamnod, Madhya Pradesh.'
    )
    # Additional profile fields
    reg_no = models.CharField(max_length=100, blank=True, default='')
    languages = models.CharField(max_length=200, blank=True, default='Hindi, English')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profile'

    def __str__(self):
        return self.name

    @classmethod
    def get_profile(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Patient(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(18)])
    address = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.mobile})"


class VisitHistory(models.Model):
    """Records each patient visit with prescription notes."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(default=timezone.now)
    diagnosis = models.CharField(max_length=500, blank=True, default='')
    prescription = models.TextField(blank=True, default='')
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        help_text='Weight in kg'
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Visit History'
        verbose_name_plural = 'Visit Histories'
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f"{self.patient.name} – {self.visit_date}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    TIME_CHOICES = [
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('01:00 PM', '01:00 PM'),
        ('01:30 PM', '01:30 PM'),
        ('05:00 PM', '05:00 PM'),
        ('05:30 PM', '05:30 PM'),
        ('06:00 PM', '06:00 PM'),
        ('06:30 PM', '06:30 PM'),
        ('07:00 PM', '07:00 PM'),
        ('07:30 PM', '07:30 PM'),
    ]

    parent_name = models.CharField(max_length=200)
    child_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    age = models.IntegerField(help_text='Child age in years')
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20, choices=TIME_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date', '-created_at']

    def __str__(self):
        return f"{self.child_name} – {self.appointment_date} at {self.appointment_time}"

    def get_status_badge(self):
        badges = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'danger',
        }
        return badges.get(self.status, 'secondary')


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, default='')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} – {self.created_at.strftime('%d %b %Y')}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(
        max_length=100, blank=True, default='bi-heart-pulse',
        help_text='Bootstrap icon class e.g. bi-heart-pulse'
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='Hospital')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or f"Gallery Image {self.pk}"


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=200)
    feedback = models.TextField()
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_name} – {self.rating}★"

    def get_stars(self):
        return range(self.rating)

    def get_empty_stars(self):
        return range(5 - self.rating)


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.question[:80]
