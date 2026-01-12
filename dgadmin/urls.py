from django.urls import path
from .views import dg_admin_dashboard, shop_list, shop_create, shop_delete, manager_list, manager_create, service_list, manager_edit, service_create, service_edit

urlpatterns = [
    path('', dg_admin_dashboard, name='dg_admin_dashboard'),
    path('shops/', shop_list, name='shop_list'),
    path('shops/add/', shop_create, name='shop_create'),
    path('shops/<int:shop_id>/delete/', shop_delete, name='shop_delete'),
    path('managers/', manager_list, name='manager_list'),
    path('managers/add/', manager_create, name='manager_create'),
    path('services/', service_list, name='service_list'),
    path('services/add/', service_create, name='service_create'),
    path('services/<int:service_id>/edit/', service_edit, name='service_edit'),

    path('managers/<int:manager_id>/edit/', manager_edit, name='manager_edit'),


    
]
