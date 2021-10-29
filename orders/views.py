from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.views.generic import (
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
from django.http import HttpResponseRedirect, request
from orders.models import Goods
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os
from django.contrib import messages


class OrderListView(ListView):
    """Listing of orders"""
    model = Order
    template_name = 'orders/order_list.html'
    # paginate_by = 10
    # filterset_class = PostFilter

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse('order_list')


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
        return reverse('order_detail', kwargs={'pk': self.object.pk})


class OrderPrintView(DetailView):
    model = Order
    template_name = 'orders/order_print.html'


class OrderSendEmail(SuccessMessageMixin, DetailView):
    model = Order
    template_name = 'orders/order_print.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        content = render_to_string('orders/order_print.html', context)
        with open('order.html', 'w', encoding='UTF-8') as static_file:
            static_file.write(content)
        msg = EmailMessage(
            _('Нава заявка від компанії ') + request.user.company_name,
            _('У додатку до цього листа надіслано заявку від компанії ') + request.user.company_name,
            'pentadatr@gmail.com',
            ['pentadatr@gmail.com',]
        )
        msg.content_subtype = "html"
        msg.attach_file('order.html')
        msg.send()
        os.remove('order.html')
        messages.success(request, _('Заявку від успішно відправлено в центральний офіс ПТ "ПЕНТАДА ТРАНС"'))
        return redirect('order_list')

    
class OrderDeleteView(SuccessMessageMixin, DeleteView):
    """Deleting of an existing order"""
    model = Order
    template_name = 'orders/order_delete.html'
    success_message = _('Заявку успішно видалено')

    def get_success_url(self):
        return reverse('order_list')