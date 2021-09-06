from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.conf import settings
from .models import Company
from references.models import Company, CustomsOffice, WarrantyProcedure, WarrantyType, VehicleType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Div, Field, Fieldset, HTML, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import Accordion, AccordionGroup, AppendedText, FormActions, InlineRadios
from django.forms.models import BaseInlineFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class CompanyForm(forms.ModelForm):
   
    class Meta:
        model = Company
        fields = (
            'name',
            'code',
            'tax',
            'address',
            'country',
            'director',
            'email',
            'phone',
            'status'
        )
    
    def __init__(self, user_id, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Div(                        
                        Fieldset(
                            "Інформація про компанію",
                            Field(
                                'name',
                                title=_('Назва компанії')                               
                            ),
                            Field(
                                'address',
                                title=_('Юридична адреса компанії')                               
                            ),
                            Field(
                                'code',
                                title=_('Код компанії в Єдиному державному реєстрі (для резидентів)')                               
                            ),
                            Field(
                                'tax',
                                title=_('Інивідуальний податковий код компанії (для резидентів)')                               
                            ),
                            Field(
                                'country',
                                title=_('Країна резиденства компанії')                               
                            )
                            # Field(
                            #     'status',
                            #     title=_('Статус компанії по відношенню до зовнішньоекономічної операції')                             
                            # )
                        ),
                        css_class='col-md-6'
                    ),
                    Div(
                        Fieldset(
                            "Контактні дані",
                            Field(
                                'director',
                                title=_("Прізвище, ім'я та по-батькові керівника компанії")                               
                            ),
                            Field(
                                'phone',
                                title=_('Контактний телефон')                               
                            ),
                            Field(
                                'email',
                                title=_('Контактна електронна поштова адреса')                               
                            ),
                            Field(
                                'status',
                                title=_('')                               
                            )
                        ),
                        css_class='col-md-6'          
                    )                 
                )
            )
        )