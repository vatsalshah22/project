import cv2
import mediapipe as mp

def get_confidence(frame):
    confidence = "97.45%"
    return confidence

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_detection.process(rgb)

    if results.detections:

        h, w, _ = frame.shape

        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            # Confidence score (0 to 1)
            confidence = detection.score[0]

            cv2.rectangle(frame,
                          (x, y),
                          (x + bw, y + bh),
                          (0, 255, 0),
                          2)

            cv2.putText(
                frame,
                f"Confidence: {confidence*100:.2f}%",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

    cv2.imshow("Face Detection Confidence", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
