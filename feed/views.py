from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
import feedparser
import re
import urllib.request
from bs4 import BeautifulSoup
from .serializers import SourceSerializer
from .models import Source

# Create your views here.

def index(request):
    return render(request, 'feed/reader.html')

# Study this
@csrf_exempt
def rest_sources(request):
    if request.method == "GET":
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SourceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

# And this
@csrf_exempt
def rest_sources_detail(request, pk):
    try:
        source = Source.objects.get(pk=pk)
    except Source.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SourceSerializer(source)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = SourceSerializer(source, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        source.delete()
        return HttpResponse()

# And this
@csrf_exempt
def rest_items(request):
    sources = Source.objects.all()

    items = []

    for source in sources:
        publisher = feedparser.parse(source.url)
        articles = publisher["items"]
        outlet = source.name
        pubDate = ''
        
        for article in articles:
            try:
                pubDate = article.published
            except:
                continue

            try:
                items.append({
                    'title': article.title,
                    'published': pubDate,
                    'link': article.link,
                    'outlet': outlet,
                })
            except KeyError:
                continue
       
    # items = list(reversed(sorted(items, key=lambda item: item["updated_parsed"])))

    return JsonResponse(items, safe=False)