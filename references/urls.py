from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('agents/<str:q>', cache_page(60*60)(views.AgentsView.as_view()), name='agents'),
    path('currencies/', views.CurrencyView.as_view(), name='currencies'),
    path('entity_types/', views.CustomsEntityTypeView.as_view(), name='entity_types'),
    path('documents/', views.DocumentView.as_view(), name='documents'),
    path('regimes/', views.CustomsRegimeView.as_view(), name='regimes'),
    path('vehicles/', views.VehicleTypeView.as_view(), name='vehicles'),
    path('customs/', views.CustomsOfficeView.as_view(), name='customs'),
    path('companies/', views.CompanyView.as_view(), name='company_list'),
    path('companies/create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('companies<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
]