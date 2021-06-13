from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from .logic import download_image, images_in_server, images_encoded, classify_face
import time, asyncio
# Create your views here.


def index(request):
    template = 'faceapi/index.html'
    context = {}
    return render(request, template, context)


def upload(request):
    '''http://localhost:8000/faceapi/upload?name={Person_Name}&img={filename/jpg}'''
    img = request.GET['img']
    name = request.GET['name']
    dir = download_image(img, name)
    return JsonResponse({'message': 'Uploaded in server at ' + dir})


async def compare(request):
    '''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
    start_time = time.time()
    server_images = images_in_server(exclude='test.jpg')
    img = request.GET['img']
    
    results = await asyncio.gather(download_image(img, 'test.jpg'), images_encoded(server_images))
    time_encode = time.time() - start_time

    test_img =  results[0]
    encoded_faces = results[1]
    
    print('time encode',time_encode)
    face_names = classify_face(test_img, encoded_faces)
    total = time.time() - start_time
    time_classify = total - time_encode
    return JsonResponse({
        'detected': face_names, 
        'time_encode': time_encode,
        'time_classify': time_classify,
        'time_total': total
        })