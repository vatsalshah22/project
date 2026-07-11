import cv2

from age import detect_age
from gender import detect_gender
from emotion import detect_emotion
from head_pose import detect_head_pose
from confidence import get_confidence

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    age = detect_age(frame)
    gender = detect_gender(frame)
    emotion = detect_emotion(frame)
    pose = detect_head_pose(frame)
    confidence = get_confidence(frame)

    cv2.putText(frame, "Age: " + age,
                (20,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.putText(frame, "Gender: " + gender,
                (20,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.putText(frame, "Emotion: " + emotion,
                (20,90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.putText(frame, "Head Pose: " + pose,
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.putText(frame, "Confidence: " + confidence,
                (20,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.imshow("Live Face Detection AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
