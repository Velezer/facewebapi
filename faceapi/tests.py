from django.test import TestCase

# Create your tests here.
import requests
def download_image(img_url):
    filename = img_url.split('/')[-1]
    img = requests.get(img_url)
    with open('faces/'+filename, 'wb') as f:
        f.write(img.content)
download_image('http://localhost:8080/faces/arief.jpg')

