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
    print('time encode',time_encode)

    test_img =  results[0]
    encoded_faces = results[1]
    
    face_names = classify_face(test_img, encoded_faces)
    total = time.time() - start_time
    time_classify = total - time_encode
    return JsonResponse({
        'detected': face_names, 
        'time_encode': time_encode,
        'time_classify': time_classify,
        'time_total': total
        })

# def get_data_from_url(url):
#     data = requests.get(url)
#     if data.status_code == 200:
#         data = data.json()
#         data = data['data']
#         for d in data:
#             d['foto'] = download_image(d['foto'])
#     return data

# def compare_krefa(request):
#     url = 'http://localhost:8080/api/people'
#     data = get_data_from_url(url)
#     encoded_faces = frec.get_encoded_faces(data)
#     img_url = request.GET['img']
#     face_names = frec.classify_face(
#         download_image(img_url, 'test.jpg'), encoded_faces)

#     return HttpResponse(face_names)
