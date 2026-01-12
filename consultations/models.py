from django.db import models
from cloudinary.models import CloudinaryField
from customers.models import Customer
from shops.models import Shop
from users.models import User
from services.models import Service
from django.db.models import Sum



class Consultation(models.Model):

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('COMPLETED', 'Completed'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='consultations'
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    visit_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_subtotal(self):
        total = self.services.aggregate(
            total=Sum('rate')
        )['total']
        return total or 0

    def __str__(self):
        return f"{self.customer.name} - {self.visit_date}"

class HairCondition(models.Model):

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='hair_condition'
    )

    last_treatment = models.CharField(max_length=200, blank=True)

    henna_or_black = models.CharField(
        max_length=20,
        choices=(('HENNA', 'Henna'), ('BLACK', 'Black')),
        blank=True
    )

    home_remedies = models.BooleanField(default=False)
    home_remedy_details = models.TextField(blank=True)

    hair_oil = models.BooleanField(default=False)
    hair_oil_details = models.TextField(blank=True)

    shampoo = models.CharField(max_length=100, blank=True)
    conditioner = models.CharField(max_length=100, blank=True)

    hair_loss = models.BooleanField(default=False)
    dandruff = models.BooleanField(default=False)

    def __str__(self):
        return f"HairCondition - {self.consultation}"



class SkinCondition(models.Model):

    SKIN_TYPE_CHOICES = (
        ('NORMAL', 'Normal'),
        ('DRY', 'Dry'),
        ('OILY', 'Oily'),
        ('COMBINATION', 'Combination'),
        ('SENSITIVE', 'Sensitive'),
    )

    SUN_EXPOSURE_CHOICES = (
        ('NEVER', 'Never'),
        ('LIGHT', 'Light (1–2 hr)'),
        ('MODERATE', 'Moderate (2–3 hr)'),
        ('EXCESSIVE', 'Excessive (3–5 hr)'),
    )

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='skin_condition'
    )

    skin_type = models.CharField(
        max_length=20,
        choices=SKIN_TYPE_CHOICES,
        blank=True
    )

    sun_exposure = models.CharField(
        max_length=20,
        choices=SUN_EXPOSURE_CHOICES,
        blank=True
    )

    acne = models.BooleanField(default=False)
    dullness = models.BooleanField(default=False)
    pigmentation = models.BooleanField(default=False)
    wrinkles = models.BooleanField(default=False)
    dryness = models.BooleanField(default=False)
    comedones = models.BooleanField(default=False)

    home_remedies = models.BooleanField(default=False)
    home_remedy_details = models.TextField(blank=True)

    night_cream = models.BooleanField(default=False)
    night_cream_details = models.TextField(blank=True)

    cleanser = models.CharField(max_length=100, blank=True)
    toner = models.CharField(max_length=100, blank=True)
    moisturiser = models.CharField(max_length=100, blank=True)
    sunscreen = models.CharField(max_length=100, blank=True)
    serum = models.CharField(max_length=100, blank=True)
    other = models.TextField(blank=True)

    def __str__(self):
        return f"SkinCondition - {self.consultation}"



class HealthCondition(models.Model):

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='health_condition'
    )
    pregnancy = models.BooleanField(default=False)
    pcod = models.BooleanField(default=False)
    thyroid = models.BooleanField(default=False)
    diabetic = models.BooleanField(default=False)
    allergies = models.BooleanField(default=False)
    allergy_details = models.TextField(blank=True)
    medication = models.BooleanField(default=False)
    medication_details = models.TextField(blank=True)
    vitamin_d_deficiency = models.BooleanField(default=False)

    def __str__(self):
        return f"HealthCondition - {self.consultation}"



class ConsultationService(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True
    )
    service_name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.service_name} - {self.rate}"

class ConsultationMedia(models.Model):

    MEDIA_TYPE_CHOICES = (
        ('BEFORE', 'Before'),
        ('AFTER', 'After'),
    )

    CATEGORY_CHOICES = (
        ('HAIR', 'Hair'),
        ('SKIN', 'Skin'),
    )

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='media'
    )

    media_file = CloudinaryField('consultation_media')

    
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consultation} - {self.media_type}"


class ConsultationSummary(models.Model):

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='summary'
    )

    suggested_treatment = models.TextField(blank=True)
    short_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary - {self.consultation}"


