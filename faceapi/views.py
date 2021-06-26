from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from .logic import *
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
        filename = await download_image(img, name)
    except Exception:
        response = JsonResponse({
            'status': 'error',
            'data': {'name': name, 'img': img},
            'message': 'Upload failed. Maybe you uploaded a non image file.'
        })
        response.status_code = 400
        return response
    
    compress_img(filename, size=(400, 400), quality=40)
    
    images = list_server_images(excludes=['test']) 
    try:
        pickling_images(images)
    except Exception:
        delete_image(name)
        response = JsonResponse({
            'status': 'error',
            'data': {'name': name, 'img': img},
            'message': "Can't pickle the image"
        })
        response.status_code = 400
        return response
    
    return JsonResponse({
        'status': 'success',
        'data': {'name': name, 'img': img},
        'message': 'Image uploaded in server'
    })


async def compare(request):
    '''http://localhost:8000/faceapi/compare?excludes={Person}&excludes={Person}&img={filename.jpg}'''
    start_time = time.perf_counter()
    img = request.GET['img']
 
    
    excludes = ['test']
    try:
        for exclude in request.GET.getlist('excludes'):
            excludes.append(exclude)
    except:
        pass

    server_images = list_server_images(excludes=excludes)

    results = await asyncio.gather(download_image(img, 'test.jpg'), get_pickled_images(server_images))
    
    try:
        compress_img(results[0], size=(200, 200), quality=24)
    except Exception as e:
        print(e)
        response = JsonResponse({
            'status': 'error',
            'message': "Maybe the image file is corrupt or the server can't download that"
        })
        response.status_code = 400
        return response
    test_img = encode_faces(results[0])
    if len(test_img) == 0:
        response = JsonResponse({
            'status': 'error',
            'message': 'No face detected.'
        })
        response.status_code = 400
        return response
    encoded_faces = results[1]

    data = classify_face(test_img, encoded_faces)

    total = time.perf_counter() - start_time
    return JsonResponse({
        'status': 'success',
        'data': data,
        'excludes': excludes[1:], 
        'response_time': total
    })
