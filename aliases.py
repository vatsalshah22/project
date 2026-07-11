import cv2
import face_recognition
import os

aliases = {
    "Vatsal": ["VS", "Vatsal Shah"],
    "Rahul": ["R. Sharma"],
    "Priya": ["P. Patel"]
}

def get_aliases(name):
    return aliases.get(name, [])

# Dictionary of aliases
aliases = {
    "Vatsal_Shah": ["Vatsal", "VS"],
    "Rahul_Sharma": ["Rahul", "R. Sharma"],
    "Priya_Patel": ["Priya", "P. Patel"]
}

known_face_encodings = []
known_face_names = []

folder = "known_faces"

# Load registered faces
for file in os.listdir(folder):
    if file.endswith(".jpg") or file.endswith(".png"):

        image = face_recognition.load_image_file(
            os.path.join(folder, file)
        )

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(file)[0])

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for (top, right, bottom, left), encoding in zip(locations, encodings):

        matches = face_recognition.compare_faces(
            known_face_encodings,
            encoding
        )

        name = "Unknown"
        alias_text = "None"

        if True in matches:

            index = matches.index(True)
            name = known_face_names[index]

            if name in aliases:
                alias_text = ", ".join(aliases[name])

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            "Name: " + name.replace("_"," "),
            (left, top-35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            "Aliases: " + alias_text,
            (left, top-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )

    cv2.imshow("Digital Identity", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
