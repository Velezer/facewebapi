import os
import pickle
import face_recognition as fr
import numpy as np
import requests
from typing import Dict, List, Tuple
from asgiref.sync import sync_to_async
from PIL import Image

THIS_DIR = os.path.dirname(__file__)
dir_faces = THIS_DIR+'/faces/'
dir_encoded = THIS_DIR+'/encoded/'


def check_if_encoded(filename: str) -> bool:
    return os.path.isfile(filename)


def save_pickle(filename: str, content):
    with open(filename, 'wb') as f:
        pickle.dump(content, f)


def read_pickle(filename: str):
    with open(filename, 'rb') as f:
        loaded = pickle.load(f)
        return loaded


@sync_to_async
def download_image(img_url: str, targetname: str = None) -> str:
    filename = img_url.split('/')[-1]
    dir = dir_faces+filename
    if targetname != None:
        dir = dir_faces+targetname
    if not dir.endswith('.jpg'):
        dir += '.jpg'
    img = requests.get(img_url)
    with open(dir, 'wb') as f:
        f.write(img.content)
    # compress_img(dir, (500,500), 50)
    compress_img(dir, size=(310, 310), quality=36)
    pickling_server_images()
    return dir


def list_server_images(exclude: str = None) -> List:
    images = []
    for dirpath, dnames, fnames in os.walk(dir_faces):
        for f in fnames:
            if f.endswith(".jpg") and exclude not in f:
                images.append(dir_faces+f)
    return images


def pickling_server_images():
    images = list_server_images('test.jpg')
    for image in images:
        filename = image.split('/')[-1]
        if not check_if_encoded(dir_encoded+filename):
            content = encode_one_face(image)
            save_pickle(dir_encoded+filename, content)


@sync_to_async
def get_pickled_images(images: List) -> Dict:
    dict = {}
    for img in images:
        nama = img.split(".")[0]
        filename = img.split('/')[-1]
        dict[nama] = read_pickle(dir_encoded+filename)

    return dict


def encode_one_face(img_path: str):
    '''return encoded one face in a image'''
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)[0]


def encode_faces(img_path: str):
    '''return encoded all face in a image'''
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)


def compress_img(img_path: str, size: Tuple, quality: int):
    img = Image.open(img_path)
    if img.size[0] > size[0] or img.size[1] > size[1]:
        img.thumbnail(size, Image.ANTIALIAS)
    img.save(img_path, quality=quality)


def classify_face(img_path: str, encoded_faces: Dict):
    faces_encoded = list(encoded_faces.values())
    known_face_names = list(encoded_faces.keys())

    # compress_img(img_path, size=(308, 308), quality=36)
    unknown_face_encodings = encode_faces(img_path)

    face_names = []
    for face_encoding in unknown_face_encodings:
        name = "Unknown"
        matches = fr.compare_faces(
            faces_encoded, face_encoding, tolerance=0.53)
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        print(face_distances)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name.split('/')[-1])

    return face_names
