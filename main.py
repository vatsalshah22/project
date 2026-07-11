import cv2

from recognition import recognize_person
from aliases import get_aliases
from linked_platforms import get_platforms
from public_mentions import get_mentions
from match_confidence import get_match_confidence

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    name = recognize_person(frame)

    aliases = get_aliases(name)
    platforms = get_platforms(name)
    mentions = get_mentions(name)
    confidence = get_match_confidence()

    y = 30

    cv2.putText(frame, f"Name: {name}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    y += 30
    cv2.putText(frame, f"Aliases: {', '.join(aliases)}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    y += 30
    cv2.putText(frame,
                f"Confidence: {confidence:.2f}%",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                2)

    y += 30
    for key, value in platforms.items():
        cv2.putText(frame,
                    f"{key}: {value}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255,255,255),
                    1)
        y += 25

    for mention in mentions:
        cv2.putText(frame,
                    "- " + mention,
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,255,255),
                    1)
        y += 25

    cv2.imshow("Digital Identity", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
