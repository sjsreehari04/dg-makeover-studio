from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bill
from consultations.models import Consultation

@login_required
def bill_list(request):
    # Filter bills based on user role
    if request.user.role == 'ADMIN':
        bills = Bill.objects.all().order_by('-created_at')
    else:
        # Managers can only see bills for their shop
        bills = Bill.objects.filter(
            consultation__shop=request.user.shop
        ).order_by('-created_at')

    return render(request, 'billing/list.html', {
        'bills': bills
    })

@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    # Security check - managers can only see bills from their shop
    if request.user.role == 'MANAGER' and bill.consultation.shop != request.user.shop:
        return redirect('bill_list')

    return render(request, 'billing/detail.html', {
        'bill': bill
    })
