import face_recognition as fr
import numpy as np

def encode_img(img_path):
    face = fr.load_image_file(img_path)
    return fr.face_encodings(face)[0]


def get_encoded_faces(data):
    encoded = {}
    
    for d in data:
        encoded[d['nama']] = encode_img(d['foto'])
    return encoded




def classify_face(img_path, encoded_faces):
    faces = encoded_faces
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = fr.load_image_file(img_path)

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_names


