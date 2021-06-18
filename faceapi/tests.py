from django.test import TestCase

# Create your tests here.
import time
import requests

img_url = 'http://kk.sttbandung.ac.id/_sepakbola/_baca_image.php?td=22&kodegb=220px-Guido_van_Rossum.jpg'
with open("c:/Users/Ace/Desktop/facewebapi/faceapi/faces/test.jpg", 'wb') as f:
    img = requests.get(img_url)
    print(f'img=')
    f.write(img.content)
    print(f'img.content=')
