from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('HAIR', 'Hair'),
        ('SKIN', 'Skin'),
        ('OTHER', 'Other'),
    )

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
