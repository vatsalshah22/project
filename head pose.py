import cv2
import mediapipe as mp
import numpy as np

def detect_head_pose(frame):
    pose = "Looking Forward"
    return pose

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    text = "No Face"

    if results.multi_face_landmarks:

        face = results.multi_face_landmarks[0]

        nose = face.landmark[1]
        left_eye = face.landmark[33]
        right_eye = face.landmark[263]
        chin = face.landmark[152]

        nose_x = int(nose.x * w)
        nose_y = int(nose.y * h)

        left_x = int(left_eye.x * w)
        right_x = int(right_eye.x * w)

        chin_y = int(chin.y * h)

        # Horizontal direction
        if nose_x < left_x + 40:
            text = "Looking Left"

        elif nose_x > right_x - 40:
            text = "Looking Right"

        else:
            # Vertical direction
            if nose_y < h * 0.40:
                text = "Looking Up"

            elif chin_y > h * 0.88:
                text = "Looking Down"

            else:
                text = "Looking Forward"

        cv2.circle(frame, (nose_x, nose_y), 5, (0, 0, 255), -1)

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Head Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
