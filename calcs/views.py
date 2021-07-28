from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .models import Warranty
from .forms import WarrantyForm
from django.utils.translation import ugettext_lazy as _


class OrderCreateView(CreateView):
    """Calculate warranty price and save object"""
    model = Warranty
    form_class = WarrantyForm
    form = None
    template_name = 'calcs/calcs.html'
    