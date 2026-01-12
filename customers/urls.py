from django.urls import path
from .views import customer_search, customer_detail, customer_create, customer_list

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('add/', customer_create, name='customer_create'),
    path('search/', customer_search, name='customer_search'),
    path('<int:customer_id>/', customer_detail, name='customer_detail'),
    
]
