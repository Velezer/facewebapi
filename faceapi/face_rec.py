import face_recognition as fr
import numpy as np
from PIL import Image


def encode_img(img_path):
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)[0]

def compress_img(img_path, size, quality):
    img = Image.open(img_path)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(img_path, quality=quality)
    

def classify_face(img_path, encoded_faces):
    faces_encoded = list(encoded_faces.values())
    known_face_names = list(encoded_faces.keys())

    compress_img(img_path, size=(308,308), quality=36)
    img = fr.load_image_file(img_path)
    unknown_face_encodings = fr.face_encodings(img)
    
    face_names = []
    for face_encoding in unknown_face_encodings:
        name = "Unknown"
        matches = fr.compare_faces(faces_encoded, face_encoding, tolerance=0.53)
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name.split('/')[-1])

    return face_names


