from django.urls import path
from .views import consultation_create, consultation_detail, hair_condition, skin_condition, health_condition, consultation_services, consultation_media_summary, consultation_drafts

urlpatterns = [
    path('add/<int:customer_id>/', consultation_create, name='consultation_create'),
    path('<int:consultation_id>/', consultation_detail, name='consultation_detail'),
    path('<int:consultation_id>/hair/', hair_condition, name='hair_condition'),
    path('<int:consultation_id>/skin/', skin_condition, name='skin_condition'),
    path('<int:consultation_id>/health/', health_condition, name='health_condition'),
    path('<int:consultation_id>/services/', consultation_services, name='consultation_services'),
    path('<int:consultation_id>/summary/', consultation_media_summary, name='consultation_summary'),
    path('drafts/', consultation_drafts, name='consultation_drafts'),
]
