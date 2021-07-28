from django.contrib import admin
from .models import Contacts, Employee
from django.utils.translation import ugettext_lazy as _


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass