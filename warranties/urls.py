from django.urls import path
from . import views


urlpatterns = [
    path('active/', views.WarrantyActiveView.as_view(), name='warranty_active'),
    path('closed/', views.WarrantyClosedView.as_view(), name='warranty_closed'),
    path('canceled/', views.WarrantyCanceledView.as_view(), name='warranty_canceled'),
]