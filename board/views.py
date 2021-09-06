from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from posts.models import Post
from news.views import NewsListView, LawsListView



class BoardView(TemplateView):
    template_name = "board/board.html"

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)              
        context['rates'] = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()
        context['eur'] = context['rates'][32]
        context['usd'] = context['rates'][26]
        context['rub'] = context['rates'][18]
        context['qa_list'] = Post.objects.filter(topic=1)
        context['news'] = NewsListView.get_queryset(self)
        context['laws'] = LawsListView.get_queryset(self)
        return context


class CurrencyRateView(TemplateView):
    template_name = "board/rates.html"

    def get_context_data(self, **kwargs):
        context = super(CurrencyRateView, self).get_context_data(**kwargs)              
        context['rates'] = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()
        return context