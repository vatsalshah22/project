import cv2
import face_recognition
import os

platforms = {
    "Vatsal": {
        "GitHub": "github.com/vatsal",
        "LinkedIn": "linkedin.com/in/vatsal"
    },
    "Rahul": {
        "GitHub": "github.com/rahul"
    }
}

def get_platforms(name):
    return platforms.get(name, {})

# Registered users and their linked platforms
user_profiles = {
    "Vatsal_Shah": {
        "GitHub": "github.com/vatsalshah",
        "LinkedIn": "linkedin.com/in/vatsalshah",
        "Email": "vatsal@example.com"
    },
    "Rahul_Sharma": {
        "GitHub": "github.com/rahulsharma",
        "LinkedIn": "linkedin.com/in/rahulsharma",
        "Email": "rahul@example.com"
    }
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

        if encodings:
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

        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.putText(
            frame,
            "Name: " + name.replace("_", " "),
            (left, top - 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        if name in user_profiles:

            profile = user_profiles[name]

            cv2.putText(
                frame,
                "GitHub: " + profile["GitHub"],
                (left, top - 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 0),
                1
            )

            cv2.putText(
                frame,
                "LinkedIn: " + profile["LinkedIn"],
                (left, top - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 0),
                1
            )

            cv2.putText(
                frame,
                "Email: " + profile["Email"],
                (left, top - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 0),
                1
            )

    cv2.imshow("Digital Identity - Linked Platforms", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
