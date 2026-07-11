import cv2
import face_recognition
import os
import numpy as np

def get_match_confidence():
    # Replace with your real confidence calculation
    return 98.75

known_face_encodings = []
known_face_names = []

folder = "known_faces"

# Load known faces
for file in os.listdir(folder):
    if file.endswith((".jpg", ".png", ".jpeg")):
        image = face_recognition.load_image_file(os.path.join(folder, file))
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

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        distances = face_recognition.face_distance(
            known_face_encodings,
            face_encoding
        )

        if len(distances) > 0:
            best_match_index = np.argmin(distances)

            distance = distances[best_match_index]

            # Convert distance to approximate confidence
            confidence = max(0, min((1 - distance) * 100, 100))

            if distance < 0.6:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            cv2.rectangle(frame,
                          (left, top),
                          (right, bottom),
                          (0, 255, 0),
                          2)

            cv2.putText(frame,
                        f"Name: {name}",
                        (left, top - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 255),
                        2)

            cv2.putText(frame,
                        f"Match Confidence: {confidence:.2f}%",
                        (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 0),
                        2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
