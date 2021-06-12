from django.test import TestCase

# Create your tests here.
import requests
import face_recognition as fr
def encode_img(img_path):
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)[0]

encode_img('')