import os
import pickle
import time
import face_recognition as fr
import numpy as np
import requests
from typing import Dict, List, Tuple
from asgiref.sync import sync_to_async
from PIL import Image

THIS_DIR = os.path.dirname(__file__)
dir_faces = ''.join([THIS_DIR, '/faces/'])
dir_encoded = ''.join([THIS_DIR, '/encoded/'])


def save_pickle(filename: str, content):
    with open(filename, 'wb') as f:
        pickle.dump(content, f)


def read_pickle(filename: str):
    with open(filename, 'rb') as f:
        loaded = pickle.load(f)
        return loaded


def delete_image(name: str):
    filenames = (''.join([dir_encoded, name, '.jpg']),
                 ''.join([dir_faces, name, '.jpg']))
    for f in filenames:
        if os.path.exists(f):
            os.remove(f)


@sync_to_async
def download_image(img_url: str, targetname: str = None) -> str:
    filename = img_url.split('/')[-1]
    filename = ''.join([dir_faces, filename])
    if targetname != None:
        filename = ''.join([dir_faces, targetname])
    if not filename.endswith('.jpg'):
        filename = ''.join([filename, '.jpg'])
    with open(filename, 'wb') as f:
        img = requests.get(img_url)
        f.write(img.content)
    return filename


def list_server_images(excludes: List = None) -> List:
    excludes = [''.join([exclude, '.jpg']) if not exclude.endswith('.jpg') else exclude for exclude in excludes ]
    for _, _, fnames in os.walk(dir_faces):
        return [''.join([dir_faces, f]) for f in fnames if f.endswith(".jpg") and f not in excludes]


def pickling_image(image):
    filename = image.split('/')[-1]
    filename = ''.join([dir_encoded, filename])
    if not os.path.isfile(filename):
        try:
            content = encode_faces(image)[0]  # encode one face
        except IndexError:
            print('No face detected')
            delete_image(filename.split('/')[-1])
        else:
            save_pickle(filename, content)


def pickling_images(images=list_server_images(excludes=['test.jpg'])):
    for image in images:
        pickling_image(image)


@sync_to_async
def get_pickled_images(images: List) -> Dict:
    dict = {}
    for img in images:
        filename = img.split('/')[-1]
        nama = filename.split(".")[0]
        filename = ''.join([dir_encoded, filename])
        dict[nama] = read_pickle(filename)

    return dict


def encode_faces(img_path: str):
    '''return encoded all face in a image'''
    face = fr.load_image_file(img_path)

    flocations = fr.face_locations(face, 2)
    result = fr.face_encodings(face, flocations, model='large')

    return result


def compress_img(img_path: str, size: Tuple, quality: int):
    img = Image.open(img_path)
    img_size = img.size
    if img_size[0] > size[0] or img_size[1] > size[1]:
        img.thumbnail(size, Image.ANTIALIAS)
    if img.mode == 'RGBA': #png A for alpha which is transparency
        img = img.convert('RGB')
    img.save(img_path, quality=quality)


def classify_face(unknown_face_encodings, encoded_faces: Dict):
    faces_encoded = list(encoded_faces.values())
    known_face_names = list(encoded_faces.keys())

    data = {
        'detected': [],
        'distances': [],
        'nearest': []
    }
    for face_encoding in unknown_face_encodings:
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        nearest = known_face_names[best_match_index]
        if face_distances[best_match_index] <= 0.62:
            name = nearest
        else:
            name = "Unknown"
        data['detected'].append(name)
        data['distances'].append(min(face_distances))
        data['nearest'].append(nearest)

    return data
