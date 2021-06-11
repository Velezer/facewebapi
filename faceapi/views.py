from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
import requests
# Create your views here.
def index(request):
    return HttpResponse('Ini Index')

def compare(request):
    id = 1
    id = str(id)
    url = 'http://localhost:8080/api/people'
    url = url + '/' + id
    data = requests.get(url)
    print(type(data))
    return HttpResponse(data)