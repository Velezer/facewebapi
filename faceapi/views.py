from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from .logic import download_image, images_in_server, images_encoded, classify_face
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
    return HttpResponse(dir)


def compare(request):
    '''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
    img = request.GET['img']
    test_img = download_image(img, 'test.jpg')

    server_images = images_in_server(exclude='test.jpg')
    encoded_faces = images_encoded(server_images)
    face_names = classify_face(test_img, encoded_faces)
    
    return JsonResponse({'detected': face_names})

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
