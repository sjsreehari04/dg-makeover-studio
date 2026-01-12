from urllib import request
from django.contrib import admin
from .models import Consultation, HairCondition, SkinCondition, HealthCondition, ConsultationService, ConsultationMedia, ConsultationSummary

class ConsultationServiceInline(admin.TabularInline):
    model = ConsultationService
    extra = 1

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'shop', 'visit_date', 'status')
    list_filter = ('shop', 'status')
    search_fields = ('customer__name', 'customer__phone')
    ordering = ('-visit_date',)
    inlines = [ConsultationServiceInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'ADMIN':
            return qs
        return qs.filter(shop=request.user.shop)
    
    def save_model(self, request, obj, form, change):
        if request.user.role == 'MANAGER':
            obj.shop = request.user.shop
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.role == 'MANAGER':
            form.base_fields.pop('shop', None)
        return form
    
    
@admin.register(HairCondition)
class HairConditionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'hair_loss', 'dandruff')

@admin.register(SkinCondition)
class SkinConditionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'acne', 'pigmentation') 

@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'pcod', 'thyroid', 'diabetic')
 
@admin.register(ConsultationService)
class ConsultationServiceAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'service_name', 'rate')
    list_filter = ('service_name',)


@admin.register(ConsultationMedia)
class ConsultationMediaAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'media_type', 'category', 'uploaded_at')
    list_filter = ('media_type', 'category')


@admin.register(ConsultationSummary)
class ConsultationSummaryAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'created_at')
