from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from consultations.models import Consultation
from customers.models import Customer
import datetime


@login_required
def dashboard_home(request):
    # 🔐 Admin must NOT see manager dashboard
    if request.user.role == 'ADMIN':
        return redirect('dg_admin_dashboard')

    # Get counts for the manager's shop
    shop = request.user.shop
    if shop:
        drafts_count = Consultation.objects.filter(shop=shop, status='DRAFT').count()
        completed_count = Consultation.objects.filter(
            shop=shop, 
            status='COMPLETED', 
            visit_date=datetime.date.today()
        ).count()
        customers_count = Customer.objects.filter(consultations__shop=shop).distinct().count()
    else:
        drafts_count = 0
        completed_count = 0
        customers_count = 0

    context = {
        'drafts_count': drafts_count,
        'customers_count': customers_count,
        'completed_count': completed_count,
    }

    return render(request, 'dashboard/home.html', context)



def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('dg_admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔑 ROLE-BASED REDIRECT
            if user.role == 'ADMIN':
                return redirect('dg_admin_dashboard')
            else:
                return redirect('dashboard')

        return render(request, 'auth/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')