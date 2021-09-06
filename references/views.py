import folium
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from folium import plugins
from PIL._imaging import display
from .models import (
    Agent, 
    Currency, 
    Document, 
    CustomsOffice, 
    CustomsEntityType, 
    CustomsRegime, 
    VehicleType,
    Company
)
from .forms import CompanyForm
from django.http import HttpResponseRedirect, request
from django.db.models import Count, Q
import decimal
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy


class AgentsView(TemplateView):
    template_name = "references/agents.html"

    def get_queryset(self):
        q = self.kwargs['q']       
        if q == "sea":
            queryset = Agent.objects.filter(vehicle__vehicle_code="10")           
        elif q == "air":
            queryset = Agent.objects.filter(vehicle__vehicle_code="40")
        elif q == "all":
            queryset = Agent.objects.all()
        elif q.isdigit():
            queryset = Agent.objects.filter(id=int(q))
            print(queryset)
        else:   
            queryset = Agent.objects.filter(country=q)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(AgentsView, self).get_context_data(**kwargs)
        figure = folium.Figure()
        m = folium.Map(
            location=[48.383022, 31.1828699],
            zoom_start=6,
            tiles='OpenStreetMap',
            control_scale=True
        )
        m.add_to(figure)

        # # add tiles to map, Create a tile layer to append on a Map
        # folium.raster_layers.TileLayer('Open Street Map').add_to(m)
        # folium.raster_layers.TileLayer('Stamen Terrain').add_to(m)
        # folium.raster_layers.TileLayer('Stamen Toner').add_to(m)
        # folium.raster_layers.TileLayer('Stamen Watercolor').add_to(m)
        # folium.raster_layers.TileLayer('CartoDB Positron').add_to(m)
        # folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(m)
        
        # # add layer control to show different maps
        # folium.LayerControl().add_to(m)
        
        # add minimap to map
        minimap = plugins.MiniMap(toggle_display=True)
        m.add_child(minimap)

        # add full screen button to map
        plugins.Fullscreen(position='topright').add_to(m)
        draw = plugins.Draw(export=True)

        # add draw tools to map
        draw.add_to(m)
        # display(m)
        for agent in self.get_queryset():
            if agent.vehicle.vehicle_code == '30':
                color = 'orange'
                icon = 'fa-truck'
            elif agent.vehicle.vehicle_code == '20':
                color='green'
                icon='fa-train'
            elif agent.vehicle.vehicle_code == '10':
                color='blue'
                icon='fa-anchor'
            elif agent.vehicle.vehicle_code == '40':
                color='purple'
                icon='fa-plane' 
            elif agent.vehicle.vehicle_code == '70':
                color='gray'
                icon='fa-gus-pump'   
            folium.Marker(
                location=[agent.latitude, agent.longitude],
                tooltip='Натисніть щоб дізнатися більше',
                popup=agent.name+' '+agent.notes,
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
        
        m = m._repr_html_()
        figure.render()
               
        context['agents'] = Agent.objects.all()
        context['country_counts'] = Agent.objects.values('country').annotate(Count('country'))
        context['sea'] = Agent.objects.filter(vehicle__vehicle_code='10')
        context['air'] = Agent.objects.filter(vehicle__vehicle_code='40')
        context['map'] = m
        return context


class CurrencyView(ListView):
    template_name ='references/currencies.html'
    context_object_name = 'currencies'
    model = Currency


class DocumentView(ListView):
    template_name ='references/documents.html'
    context_object_name = 'documents'
    model = Document


class CustomsOfficeView(ListView):
    template_name ='references/customs.html'
    context_object_name = 'customs'
    model = CustomsOffice


class CustomsEntityTypeView(ListView):
    template_name ='references/entity_types.html'
    context_object_name = 'entity_types'
    model = CustomsEntityType


class CustomsRegimeView(ListView):
    template_name ='references/regimes.html'
    context_object_name = 'regimes'
    model = CustomsRegime


class VehicleTypeView(ListView):
    template_name ='references/vehicles.html'
    context_object_name = 'vehicles'
    model = VehicleType


class CompanyView(ListView):
    template_name ='references/company_list.html'
    context_object_name = 'companies'
    model = Company
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Company.objects.all()
        else:
            return Company.objects.filter(user=self.request.user, status=True)


class CompanyCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new company"""
    model = Company
    form_class = CompanyForm
    template_name = 'references/company_create.html'
    success_url = reverse_lazy('company_list')
    success_message = _('Компанію успішно створено')

    def get_form_kwargs(self):
        kwargs = super(CompanyCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return super(CompanyCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class CompanyUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing company"""
    model = Company
    form_class = CompanyForm
    template_name = 'references/company_update.html'
    success_url = reverse_lazy('company_list')
    success_message = _('Інформацію про компанію успішно виправлено')

    def get_form_kwargs(self):
        kwargs = super(CompanyUpdateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs


class CompanyDeleteView(SuccessMessageMixin, DeleteView):
    """Deleting of an existing company"""
    model = Company
    template_name = 'references/company_delete.html'
    success_message = _('Компанію успішно видалено')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(success_url)
    
    def get_success_url(self):
        return reverse('company_list')