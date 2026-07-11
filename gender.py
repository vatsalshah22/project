import cv2

def detect_gender(frame):
    gender = "Male"
    return gender

# Face Detection Model
faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

# Gender Detection Model
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

cap = cv2.VideoCapture(0)

padding = 20

while True:
    hasFrame, frame = cap.read()

    if not hasFrame:
        break

    frameCopy = frame.copy()
    h = frame.shape[0]
    w = frame.shape[1]

    blob = cv2.dnn.blobFromImage(
        frameCopy,
        1.0,
        (300, 300),
        [104, 117, 123],
        swapRB=False
    )

    faceNet.setInput(blob)
    detections = faceNet.forward()

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.7:

            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            x1, y1, x2, y2 = box.astype(int)

            face = frame[
                max(0, y1-padding):min(y2+padding, h-1),
                max(0, x1-padding):min(x2+padding, w-1)
            ]

            if face.size == 0:
                continue

            blob = cv2.dnn.blobFromImage(
                face,
                1.0,
                (227, 227),
                MODEL_MEAN_VALUES,
                swapRB=False
            )

            genderNet.setInput(blob)
            genderPreds = genderNet.forward()

            gender = genderList[genderPreds[0].argmax()]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                frame,
                "Gender: " + gender,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

    cv2.imshow("Live Gender Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
