from django.db import models
from consultations.models import Consultation
from users.models import User


class Bill(models.Model):

    PAYMENT_MODE_CHOICES = (
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
    )

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='bill'
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_invoice_number():
        last_bill = Bill.objects.order_by('-id').first()
        if last_bill and last_bill.invoice_number:
            try:
                last_num = int(last_bill.invoice_number.split('-')[-1])
                new_num = last_num + 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1
        return f"INV-{new_num:04d}"

    def __str__(self):
        return f"Bill - {self.invoice_number or self.id} - {self.consultation} - {self.total_amount}"
