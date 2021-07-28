import folium
from django.views.generic import TemplateView, ListView
from folium import plugins
from PIL._imaging import display
from .models import Agent, Currency, Document, CustomsOffice, CustomsEntityType, CustomsRegime, VehicleType
from django.http import request
from django.db.models import Count, Q
import decimal


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