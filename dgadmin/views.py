from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from shops.models import Shop
from services.models import Service
from customers.models import Customer

@login_required
def dg_admin_dashboard(request):
    # Security check
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    # Get actual counts
    shops_count = Shop.objects.count()
    managers_count = User.objects.filter(role='MANAGER').count()
    services_count = Service.objects.filter(is_active=True).count()
    customers_count = Customer.objects.count()

    context = {
        'shops_count': shops_count,
        'managers_count': managers_count,
        'services_count': services_count,
        'customers_count': customers_count,
    }

    return render(request, 'dgadmin/dashboard.html', context)

from shops.models import Shop

@login_required
def shop_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    shops = Shop.objects.all()
    return render(request, 'dgadmin/shops/list.html', {'shops': shops})

@login_required
def shop_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    if request.method == 'POST':
        Shop.objects.create(name=request.POST.get('name'))
        return redirect('shop_list')

    return render(request, 'dgadmin/shops/create.html')

@login_required
def shop_delete(request, shop_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')

    return redirect('shop_list')

@login_required
def manager_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    managers = User.objects.filter(role='MANAGER')
    return render(request, 'dgadmin/managers/list.html', {
        'managers': managers
    })


@login_required
def manager_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    shops = Shop.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        shop_id = request.POST.get('shop')

        User.objects.create_user(
            username=username,
            password=password,
            role='MANAGER',
            shop_id=shop_id
        )

        return redirect('manager_list')

    return render(request, 'dgadmin/managers/create.html', {
        'shops': shops
    })


@login_required
def manager_edit(request, manager_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    manager = User.objects.get(id=manager_id, role='MANAGER')
    shops = Shop.objects.all()

    if request.method == 'POST':
        manager.shop_id = request.POST.get('shop')
        manager.is_active = request.POST.get('is_active') == 'on'
        manager.save()

        return redirect('manager_list')

    return render(request, 'dgadmin/managers/edit.html', {
        'manager': manager,
        'shops': shops
    })


@login_required
def service_list(request):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')

    services = Service.objects.all()
    can_edit = request.user.role == 'ADMIN'
    return render(request, 'dgadmin/services/list.html', {
        'services': services,
        'can_edit': can_edit
    })

@login_required
def service_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    if request.method == 'POST':
        Service.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            price=request.POST.get('price'),
        )
        return redirect('service_list')

    return render(request, 'dgadmin/services/create.html')

@login_required
def service_edit(request, service_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.category = request.POST.get('category')
        service.price = request.POST.get('price')
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()

        return redirect('service_list')

    return render(request, 'dgadmin/services/edit.html', {
        'service': service
    })
