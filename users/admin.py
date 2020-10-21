from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

# Admin Action Functions
def change_rating(modeladmin, request, queryset):
    queryset.update(rating = 'e')
# Action description
change_rating.short_description = "Mark Selected Products as Excellent"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display =  ['email', 'first_name', 'last_name', 'company_name', 'is_staff']
    list_filter = ['company_name', 'is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ('last_name', 'first_name', 'username', 'email', 'company_name')
    ordering = ('last_name',)
    filter_horizontal = ('groups', 'user_permissions')
    actions = [change_rating]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Персональна інформація'), {'fields': ('first_name', 'middle_name', 'last_name', 'position')}),
        (_('Інформація про компанію'), {'fields': ('company_name', 'company_code', 'company_tax', 'company_address',)}),
        (_('Дозволи'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Важливі дати'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'password1', 'password2')}
         ),
    )

admin.site.register(User, CustomUserAdmin)