from django.urls import path
from .views import bill_detail

urlpatterns = [
    path('<int:bill_id>/', bill_detail, name='bill_detail'),
]