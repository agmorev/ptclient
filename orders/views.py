from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from .models import Order
from .forms import OrderForm, GoodsFormSet, UploadDocsFormSet
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect
import os
from datetime import datetime
import firebirdsql
from sshtunnel import SSHTunnelForwarder
import pandas as pd


class OrderListView(ListView):
    """Listing of sent orders"""
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('order_list')


class OrderIssuedView(TemplateView):
    """Listing of issued orders"""
    template_name = "orders/order_issued.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # GET CONNECT TO DATABASE
        server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 3050)
                )
        server.start()
        print(server)

        conn = firebirdsql.connect(
                host='127.0.0.1',
                database='C:/MasterD/MDGarant/PentadaDB/Db/MDGARANT.FDB',
                port=3050,
                user='SYSDBA',
                password='masterkey',
                charset='UTF8'
        )

        if self.request.user.company_code != '36701373':
            edrpou = self.request.user.company_code
        else:
            edrpou = ''

        currentYear = datetime.now().year
        pd.options.display.float_format = '{:,.2f}'.format

        # GET DATA FROM DATABASE
        df = pd.read_sql('''
                    SELECT
                        GL_NUM,
                        GL_DATE_CR,
                        GL_CL_CNT,
                        GL_CL_NAME,
                        GL_CL_OKPO,
                        GL_CL_ADR,
                        GL_CAR_CNT,
                        GL_CAR_NAME,
                        GL_CAR_ADR,
                        GL_TRANS_NUM,
                        GL_DR_NAME,
                        GL_LIST_PROC,
                        GL_IN_CUS_CODE,
                        GL_OUT_CUS_CODE,
                        GG_33_01,
                        GG_31_01,
                        GG_35_01,
                        GL_SUMMA
                    FROM GARANT_REQ
                    INNER JOIN GARANT_REQ_GOODS
                    ON GARANT_REQ.IDENT=GARANT_REQ_GOODS.IDENT
                    WHERE GL_CL_OKPO LIKE '%{}' AND GL_DATE>='{}-01-01 00:00' AND GL_NUM NOT LIKE 'Ш%'
                    ORDER BY GL_NUM DESC;
                    '''.format(edrpou, currentYear), conn)

        df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)

        df = df.groupby('GL_NUM').agg({
            'GL_NUM': 'first',
            'GL_DATE_CR': 'first',
            'GL_CL_CNT': 'first',
            'GL_CL_NAME': 'first',
            'GL_CL_OKPO': 'first',
            'GL_CL_ADR': 'first',
            'GL_CAR_CNT': 'first',
            'GL_CAR_NAME': 'first',
            'GL_CAR_ADR': 'first',
            'GL_TRANS_NUM': 'first',
            'GL_DR_NAME': 'first',
            'GL_LIST_PROC': 'first',
            'GL_IN_CUS_CODE': 'first',
            'GL_OUT_CUS_CODE': 'first',
            'GG_33_01': ', '.join,
            'GG_31_01': '; '.join,
            'GG_35_01': sum,
            'GL_SUMMA': 'first',
        })

        df.fillna("-", inplace=True)

        context['df'] = df.rename(
            columns={
                'GL_NUM': 'Номер',
                'GL_DATE_CR': 'Дата',
                'GL_CL_CNT': 'Країна клієнта',
                'GL_CL_NAME': 'Клієнт',
                'GL_CL_OKPO': 'ЄДРПОУ',
                'GL_CL_ADR': 'Адреса клієнта',
                'GL_CAR_CNT': 'Країна перевізника',
                'GL_CAR_NAME': 'Перевізник',
                'GL_CAR_ADR': 'Адреса перевізника',
                'GL_TRANS_NUM': 'Т/З',
                'GL_DR_NAME': 'Водій',
                'GL_LIST_PROC': 'Режим',
                'GL_IN_CUS_CODE': 'Митниця відправлення',
                'GL_OUT_CUS_CODE': 'Митниця призначення',
                'GG_33_01': 'УКТЗЕД',
                'GG_31_01': 'Товар',
                'GG_35_01': 'Вага, кг',
                'GL_SUMMA': 'Сума гарантії'
            }, inplace=False)
        conn.close()
        server.stop()

        return context


class OrderCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new order"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('order_list')
    success_message = _('Заявку успішно створено')

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        data['goods'] = GoodsFormSet(self.request.POST or None, self.request.FILES or None)
        data['docs'] = UploadDocsFormSet(self.request.POST or None, self.request.FILES or None)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset_goods = context['goods']
        formset_docs = context['docs']
        with transaction.atomic():
            form.instance.user_id = self.request.user.id
            self.object = form.save()
            if formset_goods.is_valid():
                formset_goods.instance = self.object
                formset_goods.save()
            if formset_docs.is_valid():
                formset_docs.instance = self.object
                formset_docs.save()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing order"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_update.html'
    success_url = reverse_lazy('order_list')
    success_message = _('Заявку успішно виправлено')

    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods_form = GoodsFormSet(instance=self.object)
        docs_form = UploadDocsFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, goods_form=goods_form, docs_form=docs_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods_form = GoodsFormSet(self.request.POST, instance=self.object)
        docs_form = UploadDocsFormSet(self.request.POST, self.request.FILES, instance=form.instance)

        if (form.is_valid() and goods_form.is_valid() and docs_form.is_valid()):
            return self.form_valid(form, goods_form, docs_form)
        return self.form_invalid(form, goods_form, docs_form)

    def form_valid(self, form, goods_form, docs_form):
        self.object = form.save()
        goods_form.instance = self.object
        goods_form.save()
        docs_form.instance = self.object
        docs_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, goods_form, docs_form):
        return self.render_to_response(self.get_context_data(form=form, goods_form=goods_form, docs_form=docs_form))


class OrderCopyView(SuccessMessageMixin, CreateView):
    """Copying of an existing order"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('order_list')
    success_message = _('Заявку успішно створено')

    def get_form_kwargs(self):
        kwargs = super(OrderCopyView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods = GoodsFormSet(instance=self.object)
        docs = UploadDocsFormSet(instance=None)
        return self.render_to_response(self.get_context_data(form=form, goods=goods, docs=docs))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods = GoodsFormSet(self.request.POST, instance=self.object, save_as_new=True)
        docs = UploadDocsFormSet(self.request.POST, self.request.FILES, instance=self.object, save_as_new=True)
        if (form.is_valid() and goods.is_valid() and docs.is_valid()):
            return self.form_valid(form, goods, docs)
        return self.form_invalid(form, goods, docs)

    def form_valid(self, form, goods, docs):
        form.instance.user_id = self.request.user.id
        self.object = form.save()
        goods.instance = self.object
        goods.save()
        docs.instance = self.object
        docs.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, goods, docs):
        return self.render_to_response(self.get_context_data(form=form, goods=goods, docs=docs))


class OrderDetailView(DetailView):
    """View of details of an order"""
    model = Order
    template_name = 'orders/order_detail.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class OrderPrintView(DetailView):
    model = Order
    template_name = 'orders/order_print.html'


class OrderSendEmail(DetailView):
    '''Sending selected order by email'''
    model = Order
    template_name = 'orders/order_print.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        content = render_to_string('orders/order_print.html', context)
        with open('order.html', 'w', encoding='UTF-8') as static_file:
            static_file.write(content)
        msg = EmailMessage(
            _('Нава заявка від компанії ')+request.user.company_name,
            _('У додатку до цього листа надіслано заявку від компанії ')+request.user.company_name,
            'pentadatr@gmail.com',
            ['pentadatr@gmail.com',]
        )
        msg.content_subtype = "html"
        msg.attach_file('order.html')
        msg.send()
        os.remove('order.html')
        messages.success(request, _('Заявку успішно відправлено в центральний офіс ПТ "ПЕНТАДА ТРАНС"'))
        return redirect('order_list')


class OrderDeleteView(SuccessMessageMixin, DeleteView):
    '''Deleting of an existing order'''
    model = Order
    template_name = 'orders/order_delete.html'
    success_message = _('Заявку успішно видалено')

    def get_success_url(self):
        return reverse('order_list')