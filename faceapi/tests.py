from django.test import TestCase

# Create your tests here.
import requests
def download_image(img_url, targetname=None):
    filename = img_url.split('/')[-1]
    dir = 'faceapi/faces/'+filename
    if targetname != None:
        dir = 'faceapi/faces/'+targetname
    img = requests.get(img_url)
    with open(dir, 'wb') as f:
        f.write(img.content)
    return dir
download_image('http://localhost:8080/faces/arief.jpg')

