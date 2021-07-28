from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
import random


class Contacts(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name='contact_user')
    contact_name = models.CharField(
        _('first name'), 
        max_length=150, 
        blank=True)
    contact_email = models.EmailField(
        _('email address'), 
        blank=True)
    contact_subject = models.CharField(
        _('subject'), 
        max_length=255, 
        blank=True)
    contact_message = models.TextField(
        _('message'), 
        max_length=150, 
        blank=True)
    contact_date = models.DateTimeField(
        _('дата створення'),
        auto_now_add=True)
    
    class Meta:
        verbose_name = _('контакт')
        verbose_name_plural = _('контакти')

    def __str__(self):
        return "{} {}-{}".format(self.user.first_name, self.user.last_name, self.contact_subject)


class Employee(models.Model):
    employee_name = models.CharField(
        _('first name'), 
        max_length=150, 
        blank=True)
    employee_lastname = models.CharField(
        _('last name'), 
        max_length=150, 
        blank=True)
    employee_position = models.CharField(
        _('посада'), 
        max_length=150, 
        blank=True)
    employee_address = models.CharField(
        _('адреса'), 
        max_length=255, 
        blank=True)
    employee_phone = models.CharField(
        _('телефон'), 
        max_length=255, 
        blank=True)
    employee_email = models.EmailField(
        _('email address'), 
        blank=True)
    employee_birthday = models.DateField(
        _('дата народження'),
        blank=True,
        null=True)
    employee_status = models.CharField(
        _('сімейний стан'), 
        max_length=255, 
        blank=True)
    employee_education = models.TextField(
        _('освіта'), 
        blank=True)
    employee_profile = models.TextField(
        _('профіль'), 
        blank=True)
    employee_skills = models.CharField(
        _('досвід'), 
        max_length=255, 
        help_text=_('Ведіть Ваш досвід роботи коротко, через кому та без пробілу'),
        blank=True)
    employee_notes = models.TextField(
        _('примітки'), 
        blank=True)
    employee_image = models.ImageField(
        _('зображення'),
        upload_to='contacts/',
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('співробітник')
        verbose_name_plural = _('співробітники')

    def get_skills_list(self):
        return self.employee_skills.split(', ')
    
    def get_random_color(self):
        COLOR_CHOICES = ['primary', 'info', 'danger', 'warning', 'success']
        return random.choice(COLOR_CHOICES)
    
    def __str__(self):
        return "{} {} - {}".format(self.employee_name, self.employee_lastname, self.employee_position)