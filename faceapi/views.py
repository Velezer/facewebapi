from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from .logic import compress_img, download_image, get_pickled_images, classify_face, list_server_images, pickling_server_images
import time, asyncio
# Create your views here.


def index(request):
    template = 'faceapi/index.html'
    context = {}
    return render(request, template, context)


async def upload(request):
    '''http://localhost:8000/faceapi/upload?name={Person_Name}&img={filename/jpg}'''
    img = request.GET['img']
    name = request.GET['name']
    dir = await download_image(img, name)
    return JsonResponse({
        'status':'success',
        'message': 'Uploaded in server at ' + dir
        })


async def compare(request):
    '''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
    start_time = time.time()
    server_images = list_server_images(exclude='test.jpg')
    img = request.GET['img']
    results = await asyncio.gather(download_image(img, 'test.jpg'), get_pickled_images(server_images))
    
    test_img =  results[0]
    encoded_faces = results[1]
    
    face_names, the_distances, nearest = classify_face(test_img, encoded_faces)
    total = time.time() - start_time
    return JsonResponse({
        'detected': face_names, 
        'distances': the_distances,
        'nearest': nearest,
        'response_time': total
        })