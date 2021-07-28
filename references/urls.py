from django.contrib import admin
from django.urls import include, path
from .views import AgentsView, CurrencyView, DocumentView, CustomsOfficeView, CustomsEntityTypeView, CustomsRegimeView, VehicleTypeView


urlpatterns = [
    path('agents/<str:q>', AgentsView.as_view(), name='agents'),
    path('currencies/', CurrencyView.as_view(), name='currencies'),
    path('entity_types/', CustomsEntityTypeView.as_view(), name='entity_types'),
    path('documents/', DocumentView.as_view(), name='documents'),
    path('regimes/', CustomsRegimeView.as_view(), name='regimes'),
    path('vehicles/', VehicleTypeView.as_view(), name='vehicles'),
    path('customs/', CustomsOfficeView.as_view(), name='customs'),
]