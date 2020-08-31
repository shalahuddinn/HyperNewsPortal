import datetime
import json
from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.conf import settings
import itertools
import random


# location = '/home/shalahuddin/HyperNews Portal/HyperNews Portal/task/hypernews/news/news.json'
location = settings.NEWS_JSON_PATH


# Create your views here.
def comingsoonview(request):
    # html = "<html><body>Coming soon</body></html>"
    return HttpResponseRedirect("/news/")


class MainNewsView(View):
    # def get(self, request, *args, **kwargs):
    #     with open('/home/shalahuddin/HyperNews Portal/HyperNews Portal/task/hypernews/news/news.json', 'r') as file:
    #         data_from_json = json.load(file)
    #         sorted_news = sorted(data_from_json, key=lambda i: i['created'])
    #         groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])
    #         obj = []
    #         for k, v in groupped_news:
    #             x = {
    #                 'date': k,
    #                 'items': list(v)
    #             }
    #             obj.append(x)
    #         print(obj)
    #     context = {
    #         'objects': obj
    #     }
    #
    #     return render(request, 'news/main_news.html', context)

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('q', '')
        with open(location, 'r') as file:
            data_from_json = json.load(file)
            sorted_news = sorted(data_from_json, key=lambda i: i['created'], reverse=True)
            filtered = [k for k in sorted_news if keyword in k['title']]
            groupped_news = itertools.groupby(filtered, lambda i: i['created'][:10])
            obj = []
            for k, v in groupped_news:
                x = {
                    'date': k,
                    'items': list(v)
                }
                obj.append(x)
            # print(obj)
        context = {
            'objects': obj
        }
        return render(request, 'news/main_news.html', context)


class DetailNewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        link = kwargs['link']
        # print(settings.NEWS_JSON_PATH)
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            data_from_json = json.load(file)
            for x in data_from_json:
                if x['link'] == link:
                    context['title'] = x['title']
                    context['text'] = x['text']
                    context['created'] = x['created']
        return context


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_news.html', {})

    def post(self, request, *args, **kwargs):
        random.seed(2)
        with open(location, 'r') as file:
            data_from_json = json.load(file)

        new_news = {
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": request.POST.get('text'),
            "title": request.POST.get('title'),
            "link": random.randint(3, 100)
        }

        data_from_json.append(new_news)
        # print(data_from_json)

        with open(location, 'w') as file:
            json.dump(data_from_json, file)

        return redirect('/news/')
