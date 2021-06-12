import os
import requests
from . import face_rec as frec


def download_image(img_url, targetname=None):
    filename = img_url.split('/')[-1]
    dir = 'faceapi/faces/'+filename
    if targetname != None:
        dir = 'faceapi/faces/'+targetname
    if not dir.endswith('.jpg'):
        dir += '.jpg'
    img = requests.get(img_url)
    with open(dir, 'wb') as f:
        f.write(img.content)
    return dir


def images_in_server(exclude=None):
    '''return list'''
    images = []
    folder = "faceapi/faces/"
    for dirpath, dnames, fnames in os.walk(folder):
        for f in fnames:
            if f.endswith(".jpg") and exclude not in f:
                images.append(folder+f)
    return images


def images_encoded(images):
    '''input list; return dict'''
    dict = {}
    for img in images:
        nama = img.split(".")[0]
        dict[nama] = frec.encode_img(img)
    return dict


def classify_face(test_img, encoded_faces):
    return frec.classify_face(test_img, encoded_faces)
