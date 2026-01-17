from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError


@login_required
def customer_search(request):
    if request.user.role != 'MANAGER':
        return redirect('dg_admin_dashboard')

    customer = None
    phone = ""

    if request.method == "POST":
        phone = request.POST.get("phone")
        customer = Customer.objects.filter(phone__icontains=phone).first()

        if customer:
            return redirect('customer_detail', customer_id=customer.id)

    return render(request, 'customers/search.html', {
        'customer': customer,
        'phone': phone
    })


# @login_required
# def customer_detail(request, customer_id):
#     if request.user.role != 'MANAGER':
#         return redirect('dg_admin_dashboard')

#     customer = get_object_or_404(Customer, id=customer_id)
#     consultations = customer.consultations.all().order_by('-visit_date')

#     return render(request, 'customers/detail.html', {
#         'customer': customer,
#         'consultations': consultations
#     })

@login_required
def customer_detail(request, customer_id):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')

    customer = get_object_or_404(Customer, id=customer_id)
    consultations = customer.consultations.all().order_by('-visit_date')

    return render(request, 'customers/detail.html', {
        'customer': customer,
        'consultations': consultations
    })

@login_required
def customer_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        try:
            Customer.objects.create(name=name, phone=phone)
            messages.success(request, "Customer added successfully!")
            return redirect("customer_list")

        except IntegrityError:
            messages.error(request, "This phone number already exists. Please select existing customer.")
            return redirect("customer_create")

    return render(request, "customers/add.html")

@login_required
def customer_list(request):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')

    search_query = request.GET.get('search', '')
    customers = Customer.objects.all().order_by('-id')

    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) | Q(phone__icontains=search_query)
        )

    return render(request, 'customers/list.html', {
        'customers': customers,
        'search_query': search_query
    })