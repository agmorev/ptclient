from django.urls import path, include
from . import views


urlpatterns = [
    # Topics' patterns
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('<int:pk>/view/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/print/', views.OrderPrintView.as_view(), name='order_print'),
]