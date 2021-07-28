from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db.models import F
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    RedirectView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormMixin
# from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Order
from .forms import OrderForm
# from .filters import TopicFilter, PostFilter
from django.utils.translation import ugettext_lazy as _


class OrderListView(ListView):
    """Listing of orders"""
    model = Order
    template_name = 'orders/order_list.html'
    paginate_by = 10
    # filterset_class = PostFilter

    def get_queryset(self):
        return Order.objects.all()


class OrderCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new order"""
    model = Order
    form_class = OrderForm
    form = None
    template_name = 'orders/order_create.html'
    success_message = _('Заявку успішно створено')

    
class OrderUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing order"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_update.html'
    success_message = _('Заявку успішно виправлено')


class OrderDetailView(FormMixin, DetailView):
    """View of details of an order"""
    model = Order
    template_name = 'orders/order_detail.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    
class OrderDeleteView(SuccessMessageMixin, DeleteView):
    """Deleting of an existing order"""
    model = Order
    template_name = 'orders/order_delete.html'
    success_message = _('Заявку успішно видалено')

    def get_success_url(self):
        return reverse('order_list')