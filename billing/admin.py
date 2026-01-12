from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'total_amount', 'payment_mode', 'created_at')
    list_filter = ('payment_mode',)
