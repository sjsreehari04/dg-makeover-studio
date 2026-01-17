from django.urls import path
from .views import bill_list, bill_detail

urlpatterns = [
    path('', bill_list, name='bill_list'),
    path('<int:bill_id>/', bill_detail, name='bill_detail'),
]