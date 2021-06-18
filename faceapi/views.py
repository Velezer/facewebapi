from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from .logic import (delete_image, encode_faces, get_pickled_images, classify_face,
                    list_server_images, download_image, pickling_images)
import time
import asyncio
# Create your views here.


def index(request):
    template = 'faceapi/index.html'
    context = {}
    pickling_images()
    return render(request, template, context)


async def upload(request):
    '''http://localhost:8000/faceapi/upload?name={Person_Name}&img={filename.jpg}'''
    img = request.GET['img']
    name = request.GET['name']
    try:
        await download_image(img, name)
    except Exception:
        response = JsonResponse({
            'status': 'error',
            'data': {'name': name, 'img': img},
            'message': 'Upload failed'
        })
        response.status_code = 400
        return response
    try:
        pickling_images()
    except:
        delete_image(name)
        response = JsonResponse({
            'status': 'error',
            'data': {'name': name, 'img': img},
            'message': "Please upload a valid image"
        })
        response.status_code = 400
        return response
    return JsonResponse({
        'status': 'success',
        'data': {'name': name, 'img': img},
        'message': 'Image uploaded in server'
    })


async def compare(request):
    '''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
    start_time = time.perf_counter()
    
    server_images = list_server_images(exclude='test.jpg')
    img = request.GET['img']

    results = await asyncio.gather(download_image(img, 'test.jpg'), get_pickled_images(server_images))

    test_img = encode_faces(results[0])
    if len(test_img) == 0:
        response = JsonResponse({
            'status': 'error',
            'message': 'No face detected. Please use better quality image.'
        })
        response.status_code = 400
        return response
    encoded_faces = results[1]

    data = classify_face(test_img, encoded_faces)

    total = time.perf_counter() - start_time
    return JsonResponse({
        'status': 'success',
        'data': data,
        'response_time': total
    })
