from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'shop', 'is_active', 'is_staff')
    list_filter = ('role', 'shop', 'is_active')
    search_fields = ('username',)
