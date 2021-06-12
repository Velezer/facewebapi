from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
import requests
from . import face_rec as frec
# Create your views here.


def index(request):
    return HttpResponse('Ini Index')


def download_image(img_url, targetname=None):
    filename = img_url.split('/')[-1]
    dir = 'faces/'+filename
    if targetname != None:
        dir = 'faces/'+targetname
    img = requests.get(img_url)
    with open(dir, 'wb') as f:
        f.write(img.content)
    return dir


def get_data_from_url(url):
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        data = data['data']
        for d in data:
            d['foto'] = download_image(d['foto'])
    return data


def compare(request):
    url = 'http://localhost:8080/api/people'
    data = get_data_from_url(url)
    encoded_faces = frec.get_encoded_faces(data)
    img_url = request.GET['img']
    face_names = frec.classify_face(download_image(img_url, 'test.jpg'), encoded_faces)

    return HttpResponse(face_names)
