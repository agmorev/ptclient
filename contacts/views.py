from .models import Employee
# from .forms import UserForm, DocumentForm, VehicleForm
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


class ContactListView(ListView):
    """View the list of employee"""
    model = Employee
    context_object_name = 'contacts'
    template_name = 'contacts/contacts.html'

   
class ProfileView(DetailView):
    """View of employee data"""
    model = Employee
    # context_object_name = 'employees'
    template_name = 'contacts/profile.html'

   