from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from PIL import Image
import os
import json


from customers.models import Customer
from services.models import Service
from billing.models import Bill

from .models import (
    Consultation,
    HairCondition,
    SkinCondition,
    HealthCondition,
    ConsultationService,
    ConsultationMedia,
    ConsultationSummary
)

def process_uploaded_file(uploaded_file):
    """
    Process uploaded file, handling HEIC validation
    """
    file_name = uploaded_file.name.lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif', '.mp4', '.avi', '.mov', '.wmv']

    # Check file extension
    file_ext = os.path.splitext(file_name)[1]
    if file_ext not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {file_ext}")

    # Check file size (10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:
        raise ValueError("File too large (max 10MB)")

    return uploaded_file

# ================= CREATE CONSULTATION =================

@login_required
def consultation_create(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    consultation = Consultation.objects.create(
        customer=customer,
        shop=request.user.shop,
        created_by=request.user,
        visit_date=timezone.now().date(),
        status='DRAFT'
    )

    return redirect('consultation_detail', consultation_id=consultation.id)


# ================= CONSULTATION DETAIL =================

# @login_required
# def consultation_detail(request, consultation_id):
#     consultation = get_object_or_404(Consultation, id=consultation_id)

#     if request.method == 'POST' and request.POST.get('action') == 'complete':
#         consultation.status = 'COMPLETED'
#         consultation.save()
#         return redirect('consultation_detail', consultation_id=consultation.id)

#     try:
#         hair = consultation.hair_condition
#     except:
#         hair = None

#     try:
#         skin = consultation.skin_condition
#     except:
#         skin = None

#     try:
#         health = consultation.health_condition
#     except:
#         health = None

#     return render(request, 'consultations/detail.html', {
#         'consultation': consultation,
#         'hair': hair,
#         'skin': skin,
#         'health': health
#     })
@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST' and request.POST.get('action') == 'complete':
        consultation.status = 'COMPLETED'
        consultation.save()
        return redirect('consultation_detail', consultation_id=consultation.id)

    hair = getattr(consultation, 'hair_condition', None)
    skin = getattr(consultation, 'skin_condition', None)
    health = getattr(consultation, 'health_condition', None)

    # 🔥 THIS IS THE KEY PART
    before_images = consultation.media.filter(media_type='BEFORE')
    after_images = consultation.media.filter(media_type='AFTER')

    return render(request, 'consultations/detail.html', {
        'consultation': consultation,
        'hair': hair,
        'skin': skin,
        'health': health,
        'before_images': before_images,
        'after_images': after_images,
    })

# ================= HAIR CONDITION =================

@login_required
def hair_condition(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    hair, _ = HairCondition.objects.get_or_create(consultation=consultation)

    if request.method == 'POST':
        hair.last_treatment = request.POST.get('last_treatment', '')
        hair.henna_or_black = request.POST.get('henna_or_black', '')
        hair.home_remedies = bool(request.POST.get('home_remedies'))
        hair.home_remedy_details = request.POST.get('home_remedy_details', '')
        hair.hair_oil = bool(request.POST.get('hair_oil'))
        hair.hair_oil_details = request.POST.get('hair_oil_details', '')
        hair.shampoo = request.POST.get('shampoo', '')
        hair.conditioner = request.POST.get('conditioner', '')
        hair.hair_loss = bool(request.POST.get('hair_loss'))
        hair.dandruff = bool(request.POST.get('dandruff'))
        hair.save()

        return redirect('consultation_detail', consultation_id=consultation.id)

    return render(request, 'consultations/hair_condition.html', {
        'consultation': consultation,
        'hair': hair
    })


# ================= SKIN CONDITION =================

@login_required
def skin_condition(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    skin, _ = SkinCondition.objects.get_or_create(consultation=consultation)

    if request.method == 'POST':
        skin.skin_type = request.POST.get('skin_type', '')
        skin.sun_exposure = request.POST.get('sun_exposure', '')
        skin.acne = bool(request.POST.get('acne'))
        skin.dullness = bool(request.POST.get('dullness'))
        skin.pigmentation = bool(request.POST.get('pigmentation'))
        skin.wrinkles = bool(request.POST.get('wrinkles'))
        skin.dryness = bool(request.POST.get('dryness'))
        skin.comedones = bool(request.POST.get('comedones'))
        skin.home_remedies = bool(request.POST.get('home_remedies'))
        skin.home_remedy_details = request.POST.get('home_remedy_details', '')
        skin.night_cream = bool(request.POST.get('night_cream'))
        skin.night_cream_details = request.POST.get('night_cream_details', '')
        skin.cleanser = request.POST.get('cleanser', '')
        skin.toner = request.POST.get('toner', '')
        skin.moisturiser = request.POST.get('moisturiser', '')
        skin.sunscreen = request.POST.get('sunscreen', '')
        skin.serum = request.POST.get('serum', '')
        skin.other = request.POST.get('other', '')
        skin.save()

        return redirect('consultation_detail', consultation_id=consultation.id)

    return render(request, 'consultations/skin_condition.html', {
        'consultation': consultation,
        'skin': skin
    })


# ================= HEALTH CONDITION =================

@login_required
def health_condition(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    health, _ = HealthCondition.objects.get_or_create(consultation=consultation)

    if request.method == 'POST':
        health.pregnancy = bool(request.POST.get('pregnancy'))
        health.pcod = bool(request.POST.get('pcod'))
        health.thyroid = bool(request.POST.get('thyroid'))
        health.diabetic = bool(request.POST.get('diabetic'))
        health.allergies = bool(request.POST.get('allergies'))
        health.allergy_details = request.POST.get('allergy_details', '')
        health.medication = bool(request.POST.get('medication'))
        health.medication_details = request.POST.get('medication_details', '')
        health.vitamin_d_deficiency = bool(request.POST.get('vitamin_d_deficiency'))
        health.save()

        return redirect('consultation_detail', consultation_id=consultation.id)

    return render(request, 'consultations/health_condition.html', {
        'consultation': consultation,
        'health': health
    })


# ================= SERVICES & BILLING =================

@login_required
def consultation_services(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    services = Service.objects.filter(is_active=True)

    if request.method == 'POST':
        service_ids = request.POST.getlist('services[]')
        custom_prices = {}
        
        # Extract custom prices from POST data
        for key, value in request.POST.items():
            if key.startswith('price_'):
                service_id = key.replace('price_', '')
                try:
                    custom_prices[service_id] = Decimal(value)
                except (ValueError, TypeError):
                    pass
        
        discount = Decimal(request.POST.get('discount', 0) or 0)
        action = request.POST.get('action')

        consultation.services.all().delete()

        for sid in service_ids:
            service = Service.objects.get(id=sid)
            # Use custom price if provided, otherwise use default service price
            rate = custom_prices.get(str(sid), service.price)
            ConsultationService.objects.create(
                consultation=consultation,
                service=service,
                service_name=service.name,
                rate=rate
            )

        consultation.status = 'DRAFT'
        consultation.save()

        if action == 'draft':
            return redirect('consultation_detail', consultation_id=consultation.id)

        if action == 'generate_bill':
            subtotal = consultation.calculate_subtotal()
            total_amount = subtotal - discount
            # Create bill if not exists
            bill, created = Bill.objects.get_or_create(
                consultation=consultation,
                defaults={
                    'subtotal': subtotal,
                    'discount': discount,
                    'total_amount': total_amount,
                    'payment_mode': 'CASH',
                    'created_by': request.user
                }
            )
            # Update values in case bill already existed
            bill.subtotal = subtotal
            bill.discount = discount
            bill.total_amount = total_amount
            bill.save()
            return redirect('bill_detail', bill_id=bill.id)

        if action == 'complete':
            return redirect('consultation_summary', consultation_id=consultation.id)

    existing_services = consultation.services.all()
    return render(request, 'consultations/services.html', {
        'consultation': consultation,
        'services': services,
        'existing_services': existing_services,
        'existing_services_json': json.dumps([
            {'service_id': es.service.id, 'rate': float(es.rate)} 
            for es in existing_services
        ])
    })


# ================= PHOTOS & SUMMARY =================

@login_required
def consultation_media_summary(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    # Check if services have been selected before allowing access to summary
    if not consultation.services.exists():
        return redirect('consultation_services', consultation_id=consultation.id)

    summary, _ = ConsultationSummary.objects.get_or_create(consultation=consultation)

    if request.method == 'POST':
        summary.suggested_treatment = request.POST.get('suggested_treatment', '')
        summary.short_summary = request.POST.get('short_summary', '')
        summary.save()

        before_files = request.FILES.getlist('before_media')
        after_files = request.FILES.getlist('after_media')

        # Process before files
        for file in before_files:
            try:
                processed_file = process_uploaded_file(file)
                ConsultationMedia.objects.create(
                    consultation=consultation,
                    media_file=processed_file,
                    media_type='BEFORE',
                    category='HAIR'
                )
            except ValueError as e:
                # For now, we'll skip invalid files but could add error handling
                continue

        # Process after files
        for file in after_files:
            try:
                processed_file = process_uploaded_file(file)
                ConsultationMedia.objects.create(
                    consultation=consultation,
                    media_file=processed_file,
                    media_type='AFTER',
                    category='HAIR'
                )
            except ValueError as e:
                # For now, we'll skip invalid files but could add error handling
                continue

        # Generate bill automatically when summary is saved
        subtotal = consultation.calculate_subtotal()
        bill, created = Bill.objects.get_or_create(
            consultation=consultation,
            defaults={
                'subtotal': subtotal,
                'discount': Decimal('0'),
                'total_amount': subtotal,
                'payment_mode': 'CASH',
                'created_by': request.user
            }
        )
        # Update values in case bill already existed
        if not created:
            bill.subtotal = subtotal
            bill.discount = Decimal('0')
            bill.total_amount = subtotal
            bill.save()

        consultation.status = 'COMPLETED'
        consultation.save()

        return redirect('consultation_detail', consultation_id=consultation.id)

    media = consultation.media.all()

    return render(request, 'consultations/summary.html', {
        'consultation': consultation,
        'summary': summary,
        'media': media
    })


# ================= CONSULTATION DRAFTS =================

@login_required
def consultation_drafts(request):
    drafts = Consultation.objects.filter(status='DRAFT', shop=request.user.shop)
    return render(request, 'consultations/drafts.html', {'drafts': drafts})
