import cv2
from deepface import DeepFace

def detect_emotion(frame):
    emotion = "Happy"
    return emotion

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    try:
        # Analyze emotion
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False
        )

        emotion = result[0]['dominant_emotion']

        # Display emotion on screen
        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    except Exception as e:
        print(e)

    cv2.imshow("Live Emotion Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
