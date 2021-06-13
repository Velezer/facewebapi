import os
import pickle
import requests
from . import face_rec as frec
from asgiref.sync import sync_to_async

THIS_DIR = os.path.dirname(__file__)


@sync_to_async
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


def check_if_encoded(filename):
    return os.path.isfile(filename)


def save_file_b(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)


def save_pickle(filename, content):
    with open(filename, 'wb') as f:
        pickle.dump(content, f)


def read_pickle(filenam):
    with open(filenam, 'rb') as f:
        loaded = pickle.load(f)
        print(loaded)
        return loaded


def read_file_b(filename):
    with open(filename, 'rb') as f:
        return f


def images_in_server(exclude=None):
    '''return list'''
    images = []
    folder = "faceapi/faces/"
    for dirpath, dnames, fnames in os.walk(folder):
        for f in fnames:
            if f.endswith(".jpg") and exclude not in f:
                images.append(folder+f)
    return images


@sync_to_async
def images_encoded(images):
    '''input list; return dict'''
    dict = {}
    for img in images:
        nama = img.split(".")[0]
        filename = img.split('/')[-1]
        if not check_if_encoded(THIS_DIR+'/encoded/'+filename):
            dict[nama] = frec.encode_img(img)
            save_pickle(THIS_DIR+'/encoded/'+filename, dict[nama])
            # dict[nama] = read_pickle(THIS_DIR+'/encoded/'+filename)
            continue
        
        dict[nama] = read_pickle(THIS_DIR+'/encoded/'+filename)

    return dict


def classify_face(test_img, encoded_faces):
    return frec.classify_face(test_img, encoded_faces)
