from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
import requests
from . import face_rec as frec
# Create your views here.
def index(request):
    return HttpResponse('Ini Index')

def get_data_from_url(url):
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        data = data['data']
    return data

def compare(request, img_path):
    url = 'http://localhost:8080/api/people'
    data = get_data_from_url(url)
    encoded_faces = frec.get_encoded_faces(data)
    face_names = frec.classify_face(img_path, encoded_faces)
    
    
    return HttpResponse(data)