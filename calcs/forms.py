from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.conf import settings
from .models import Warranty
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Div, Field, Fieldset, HTML, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import Accordion, AccordionGroup, AppendedText, FormActions, InlineRadios
from django.forms.models import BaseInlineFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _


class WarrantyForm(forms.ModelForm):

    VEHICLE_CHOICES = (
        ('1', 'Автомобільний'),
        ('2', 'Залізничний'),
        ('3', 'Морський/річковий'),
        ('4', 'Трубопровідний'),
        ('5', 'Авіаційний'),
    )

    vehicle = forms.ChoiceField(
        label=_('Вид транспорту'),
        required=False,
        choices=VEHICLE_CHOICES)

    class Meta:
        model = Warranty
        fields = (
            'user',
            'order_number',
            # 'order_created',
            # 'order_updated',
            'order_regime',
            'order_vehicle',
        )
    
    def __init__(self, *args, **kwargs):
        super(WarrantyForm, self).__init__(*args, **kwargs)
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
                                title=_(
                                    '''Заповнюється на розсуд клієнта для зручності ведення обліку'''
                                )                               
                            )
                        ),
                        css_class='col-md-5'                 
                    ),
                    
                )
            ),
            Fieldset(
                "",
                Row(
                    Div(                        
                        Fieldset(
                            "",
                            Field(
                                'order_regime',
                                title=_(
                                    '''Зазначаються дані про наявність (відсутність) супроводжуваного багажу та ручної поклажі, а також про кількість їх місць'''
                                )                               
                            )
                        ),
                        css_class='col-md-5'                 
                    ),
                    Div(
                        Fieldset(
                            "",
                            Field(
                                'order_vehicle',
                                placeholder=_('Кількість місць'),
                                title=_(
                                    '''Зазначаються дані про наявність (відсутність) несупроводжуваного багажу і про кількість його місць'''
                                )
                            )
                        ),
                        css_class='col-md-5'
                    )
                )
            ),
            HTML('<hr>'),
            Fieldset(
                _('1. Відправник вантажу'),
                Field(
                    'order_regime',
                    title=_(
                        '''Обирається з переліку, який створено користувачем у власному профілі'''
                    )
                ),
                Field(
                    'order_vehicle',
                    title=_(
                        '''Країна, з якої прибув (згідно з документами, що підтверджують маршрут прямування, у разі їх наявності)'''
                    )
                ),
                # Field(
                #     'arrival',
                #     title=_(
                #         '''Країна, до якої прямує (згідно з документами, що підтверджують маршрут прямування, у разі їх наявності)'''
                #     )
                # ),
            ),
            # Fieldset(
            #     "Зі мною прямують неповнолітні діти",
            #     Field(
            #         'kids_number',
            #         placeholder=_('Кількість дітей'),
            #         title=_(
            #             '''Наявність (відсутність) дітей віком до 16 років, які супроводжуються громадянином і перетинають митний кордон України разом з ним, із зазначенням кількості (цифрами та словами) таких дітей'''
            #         )
            #     ),
            #     css_class='col-md-4'
            # ),
            # HTML('<hr>'),
            # Fieldset(
            #     _('2. Відомості про спосіб переміщення товарів'),
            #     Row(
            #         Div(
            #             Fieldset(
            #                 _("2.1. Супроводжуваний багаж, ручна поклажа"),
            #                 Field(
            #                     'accamp_number',
            #                     placeholder=_('Кількість місць'),
            #                     title=_(
            #                         '''Зазначаються дані про наявність (відсутність) супроводжуваного багажу та ручної поклажі, а також про кількість їх місць'''
            #                     )
            #                 ),
            #             ),
            #             css_class='col-md-4'
            #         ),
            #         Div(
            #             Fieldset(
            #                 _("2.2. Несупроводжуваний багаж"),
            #                 Field(
            #                     'nonaccamp_number',
            #                     placeholder=_('Кількість місць'),
            #                     title=_(
            #                         '''Зазначаються дані про наявність (відсутність) несупроводжуваного багажу і про кількість його місць'''
            #                     )
            #                 ),
            #             ),
            #             css_class='col-md-4'
            #         ),
            #         Div(
            #             Fieldset(
            #                 _("2.3. Вантажне відправлення"),
            #                 Field(
            #                     'cargo_number',
            #                     placeholder=_('Кількість місць'),
            #                     title=_(
            #                         '''Заповнюється у разі відправлення громадянином товарів за межі митної території України у вантажному відправленні'''
            #                     )
            #                 ),
            #             ),
            #             css_class='col-md-4'
            #         ),
            #     ),
            # ),
            # HTML('<hr>'),
            # Fieldset(
            #     _('3. Відомості про наявність товарів'),
            #     Fieldset(
            #         _("3.2. Транспортний засіб особистого користування"),
            #         Field(
            #             'vehicle',
            #             title=_(
            #                 '''Обирається з переліку, який створено користувачем у власному профілі'''
            #             )
            #         ),
            #         InlineRadios('purpose'),
            #         title=_(
            #             '''Наводяться детальні відомості про транспортний засіб особистого користування, що тимчасово ввозиться на митну територію України, ввозиться на митну територію України з метою транзиту або зворотно вивозиться за межі митної території України. У полі для зазначення мети переміщення транспортного засобу особистого користування через митний кордон України ставиться позначка в потрібній рамці'''
            #         )
            #     ),
            #     Fieldset(
            #         _('''3.3. Товари, переміщення яких через державний кордон України
            #         обмежено (здійснюється за дозвільними документами, що видаються
            #         органами виконавчої влади) або заборонено'''),
            #         InlineRadios(
            #             'limited',
            #             title=_(
            #                 '''Заповнення здійснюється шляхом проставлення позначки у відповідній рамці: „Так” - за наявності товарів переміщення, „Ні” - за їх відсутності'''
            #             )
            #         ),
            #     ),
            # ),
            # HTML('<hr>'),
            # Fieldset(
            #     _('''4. Відомості про товари, що підлягають обов’язковому письмовому
            #       декларуванню та/або оподаткуванню митними платежами, товари,
            #       переміщення яких через державний кордон України заборонено
            #       або здійснюється за дозвільними документами, що видаються
            #       органами виконавчої влади, та інші товари, що декларуються
            #       письмово за бажанням громадянина або на вимогу митного органу'''),
            # ),
            # HTML('<hr>'),
        )