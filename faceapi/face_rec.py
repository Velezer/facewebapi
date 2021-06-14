import face_recognition as fr
import numpy as np
import time
from PIL import Image
from numpy.core.fromnumeric import size
def encode_img(img_path):
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)[0]

def compress_img(img_path):
    img = Image.open(img_path)
    size = 100,100
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(img_path, quality=40)
    

def classify_face(img_path, encoded_faces):
    faces = encoded_faces
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    start = time.time()
    # compress
    compress_img(img_path)
    # endcompress
    img = fr.load_image_file(img_path)
    print(time.time()-start)
    unknown_face_encodings = fr.face_encodings(img)
    print(time.time()-start)
    
    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        print(face_distances)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name.split('/')[-1])

    return face_names


