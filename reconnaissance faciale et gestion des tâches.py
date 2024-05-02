import cv2 as cv
import face_recognition
import yaml
import os
import json
import pyttsx3

class GestionTaches:
    def __init__(self, fichier):
        self.employes = {}
        self.fichier = fichier

    def afficher_taches(self, employe):
        taches = self.employes.get(employe, [])
        if taches:
            return f"Tâches pour {employe}: {taches}"
        else:
            return f"{employe} n'a aucune tâche attribuée."
    

    def charger_taches(self):
        try:
            with open(self.fichier, 'r') as f:
                self.employes = json.load(f)
        except FileNotFoundError:
            pass


# Load known faces and their encodings from the YAML file
def load_known_faces(yaml_file):
    with open(yaml_file, 'r') as yaml_in:
        encoding_data = yaml.safe_load(yaml_in)

    known_face_encodings = [item['encoding'] for item in encoding_data]
    known_face_names = [os.path.splitext(item['filename'])[0] for item in encoding_data]

    return known_face_encodings, known_face_names

# Recognize faces using the camera
def recognize_faces(known_face_encodings, known_face_names):
    cap = cv.VideoCapture(0)

    ret, frame = cap.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    engine = pyttsx3.init()  # Initialize the text-to-speech engine

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Call the function switch with the detected name
            resultat = switch(name)
            print(resultat)

            # Speak the greeting message
            engine.say(f"Bonjour monsieur {name}")
            engine.runAndWait()

        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv.imshow('Video', frame)
    cv.waitKey(0)  # Wait indefinitely for a key press before closing the window

    cap.release()
    cv.destroyAllWindows()

gestion_taches = GestionTaches("taches.json")
gestion_taches.charger_taches()

# Function to display tasks based on the detected name
def switch(known_face_names):
    if known_face_names:
        return gestion_taches.afficher_taches(known_face_names)
    else: 
        return "Unknown face."


if __name__ == "__main__":
    yaml_file_path = "C:/Users/Hasnaoui/Downloads/yamlf1"  # Update with the path to your YAML file
    known_face_encodings, known_face_names = load_known_faces(yaml_file_path)

    if known_face_encodings and known_face_names:
        result = recognize_faces(known_face_encodings, known_face_names)
        print(result)
    else:
        print("No known faces found. Please ensure your YAML file is properly configured.")
