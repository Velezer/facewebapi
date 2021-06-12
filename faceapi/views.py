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
        for d in data:
            d['foto'] = download_image(d['foto']) 
    return data

def download_image(img_url):
    filename = img_url.split('/')[-1]
    dir = 'faces/'+filename
    img = requests.get(img_url)
    with open(dir, 'wb') as f:
        f.write(img.content)
    return dir

def compare(request, img_path):
    url = 'http://localhost:8080/api/people'
    data = get_data_from_url(url)
    encoded_faces = frec.get_encoded_faces(data)
    face_names = frec.classify_face(img_path, encoded_faces)
    
    
    return HttpResponse(data)