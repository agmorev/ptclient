from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.conf import settings
from .models import Order, Goods, UploadDocs
from references.models import Company, CustomsOffice, WarrantyProcedure, CustomsRegime, WarrantyType, VehicleType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Div, Field, Fieldset, HTML, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import Accordion, AccordionGroup, AppendedText, FormActions, InlineRadios
from django.forms.models import BaseInlineFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class WarrantiesModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return object.name


class СustomsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %s" % (object.office_code, object.office_name)


class CompanyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return object.name


class RegimeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s.%s %s" % (object.short_name, object.code, object.name)


class ProcedureModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %s" % (object.code, object.name)


class DepartureModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %s" % (object.office_code, object.office_name)


class DestinationModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %s" % (object.office_code, object.office_name)


class VehicleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return object.vehicle_name


class OrderForm(forms.ModelForm):
    warranty_type = WarrantiesModelChoiceField(
        label='',
        empty_label=None,
        queryset=WarrantyType.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    customs = СustomsModelChoiceField(
        label=_('Бенефіціар'),
        queryset=CustomsOffice.objects.filter(office_code__endswith='000'),
        empty_label=_('Оберіть митницю...'),
        widget=forms.Select(),
        required=True
    )
    principal = CompanyModelChoiceField(
        label=_('Принципал'),
        queryset=Company.objects.none(),
        empty_label=_('Оберіть компанію...'),
        widget=forms.Select(),
        required=True
    )
    procedure = ProcedureModelChoiceField(
        label=_('Процедура'),
        queryset=WarrantyProcedure.objects.all(),
        empty_label=_('Оберіть процедуру...'),
        widget=forms.Select(),
        required=True
    )
    regime = RegimeModelChoiceField(
        label=_('Режим'),
        queryset=CustomsRegime.objects.filter(status=True),
        empty_label=_('Оберіть режим...'),
        widget=forms.Select(),
        required=False
    )
    customs_departure = DepartureModelChoiceField(
        label=_('Відправлення'),
        queryset=CustomsOffice.objects.all(),
        empty_label=_('Оберіть митницю відправлення...'),
        widget=forms.Select(),
        required=False
    )
    customs_destination = DestinationModelChoiceField(
        label=_('Призначення'),
        queryset=CustomsOffice.objects.all(),
        empty_label=_('Оберіть митницю призначення...'),
        widget=forms.Select(),
        required=False
    )
    vehicle = VehicleModelChoiceField(
        label=_('Транспорт'),
        queryset=VehicleType.objects.all(),
        empty_label=_('Оберіть вид транспорту...'),
        widget=forms.Select(),
        required=True
    )

    class Meta:
        model = Order
        fields = (
            'order_number',
            'order_created',
            'warranty_type',
            'customs',
            'principal',
            'procedure',
            'regime',
            'vehicle',
            'customs_departure',
            'customs_destination',
            'expired_date'
        )
    
    def __init__(self, user_id, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['principal'].queryset = Company.objects.filter(user_id=user_id)
        self.fields['order_created'].label = _('від')
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<hr>'),
            Fieldset(
                "",
                Row(
                    Div(                        
                        Fieldset(
                            "",
                            Field(
                                'order_number',
                                title=_('Номер заявки для зручності ведення обліку')                               
                            )
                        ),
                        css_class='col-md-offset-4 col-md-2'
                    ),
                    Div(
                        Fieldset(
                            "",
                            Field(
                                'order_created',
                                title=_('Дата створення заявки'),
                                placeholder=_("дд.мм.рррр"), 
                                css_class='form-control datepicker', 
                                active=True                               
                            )
                        ),
                        css_class='col-md-2'                 
                    )                  
                )
            ),
            HTML('<hr>'),
            Fieldset(
                "",
                Row(
                    Div(
                        Fieldset(
                            "Клієнт",
                            HTML('<p>{{user.company_name}} ({{user.company_code}})</p>'),
                            HTML('<p>{{user.company_address}}</p>'),
                            HTML('<p>{{user.phone}}</p>'),                           
                        ),
                        css_class='col-md-6'
                    ),
                    Div(
                        Fieldset(
                            "Вид послуги",
                            Field(
                                'warranty_type',
                                title=_('Оберіть пакет гарантування')                             
                            )                            
                        ),
                        css_class='col-md-6'
                    )
                )
            ),
            HTML('<hr>'),
            Fieldset(
                _('1. Учасники процедури'),               
                Field(
                    'customs',
                    title=_('Митний орган, на користь якого забезпечується сплата митних платежів'),
                ),
                Field(
                    'principal',
                    title=_('Компанія, яка є особою відповідальною за сплату митних платежів та дотримання умов митного режиму'),                              
                ),
                css_class='col-md-6'
            ),
            Fieldset(
                _('2. Процедура гарантування'),               
                Field(
                    'procedure',
                    title=_('Митна процедура, за якою гарантується сплата митних платежів'),
                ),
                Field(
                    'regime',
                    title=_('Митна режим, в якому розміщуються товари із вимогою забезпечення сплати митних платежів'),
                ),
                Field(
                    'customs_departure',
                    title=_('Підрозділ митного органу, в якому починається переміщення за процедурою гарантування'),                              
                ),
                Field(
                    'customs_destination',
                    title=_('Підрозділ митного органу, в якому закінчується переміщення за процедурою гарантування'),                              
                ),
                Field(
                    'vehicle',
                    title=_('Транспортний засіб, в якому переміщуються товари, що підлягають гарантуванню'),                              
                ),
                Field(
                    'expired_date',
                    title=_('Дата закінчення дії фінансової гарантії'), 
                    placeholder=_("дд.мм.рррр"), 
                    css_class='form-control datepicker', 
                    active=True                       
                ),               
            ),
            HTML('<hr>'),
            Fieldset(
                _('3. Інформація про товари')
            )           
        )


class GoodsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoodsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Div(
                        Field(
                            'name',
                            placeholder=_('Найменування товару'),
                            title=_('Зазначається опис товару')
                        ),
                        css_class='col-md-3',

                    ),
                    Div(
                        Field(
                            'code',
                            placeholder=_('Код товару'),
                            title=_('Зазначається код товару згідно з УКТЗЕД 10 знаків')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'number',
                            placeholder=_('Вага, кг'),
                            title=_(
                                '''Зазначається вага товару в кг.''')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'addnumber',
                            placeholder=_('Кількість'),
                            title=_(
                                '''Зазначається кількість товару в додаткових одиницях виміру''')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'duties',
                            placeholder=_('Платежі, грн'),
                            title=_(
                                '''Зазначається сума митних платежів, що підлягає гарантуванню''')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'DELETE',
                            title=_(
                                'В разі проставлення позначки після зберігання заявки товар буде видалено із переліку')
                        ),
                        css_class='col-md-1 tools'
                    ),
                ),
                css_class='formset'
            ),     
        )

    class Meta:
        model = Goods
        exclude = ()


class UploadDocsForm(forms.ModelForm):

    # doc_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = UploadDocs
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UploadDocsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Div(    
                        Field(
                            'doc_file',      
                            title=_('Завантажити файл, що містить документ'),  
                            # css_class='fileinput-new',
                            css_id='customFile'                                   
                        ),
                        css_class='col-md-6'
                    ),
                    Div(     
                        Field(
                            'doc_name',
                            placeholder=_('Опис документу'),
                            title=_('Зазначається опис документу, що завантажується'),                            
                        ), 
                        css_class='col-md-5'
                    ),
                    Div(               
                        Field(
                            'DELETE',
                            title=_(
                                'В разі проставлення позначки після зберігання документ буде видалено із переліку'),                           
                        ),
                        css_class='col-md-1'
                    ),
                ),
                
                css_class='formset'               
            )           
        )


GoodsFormSet = inlineformset_factory(
    Order, Goods,
    form=GoodsForm,
    fields=(
        'name',
        'code',
        'number',
        'addnumber',
        'duties'
    ),
    extra=1,
    can_delete=True
)


UploadDocsFormSet = inlineformset_factory(
    Order, UploadDocs,
    form=UploadDocsForm,
    fields=(
        'doc_file',
        'doc_name',
    ),
    extra=1,
    can_delete=True
)
