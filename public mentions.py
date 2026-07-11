import cv2
import face_recognition
import numpy as np
import os

mentions = {
    "Vatsal": [
        "Won AI Hackathon",
        "Cyber Security Workshop Speaker"
    ],
    "Rahul": [
        "Python Competition Finalist"
    ]
}

def get_mentions(name):
    return mentions.get(name, [])

# --- STEP 1: INITIALIZE THE DIGITAL IDENTITY DATABASE ---
KNOWN_DIR = "known_identities"
known_face_encodings = []
known_face_identities = []

print("[-] Loading Digital Identity Database...")
if not os.path.exists(KNOWN_DIR):
    os.makedirs(KNOWN_DIR)
    print(f"[!] Created '{KNOWN_DIR}' directory. Please add profile images and restart.")

# Scan the folder for images and extract face encodings (digital fingerprints)
for filename in os.listdir(KNOWN_DIR):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(KNOWN_DIR, filename)
        
        # Load image and generate encoding
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            # Use the filename (minus extension) as the identity name
            identity_name = os.path.splitext(filename)[0].replace("_", " ").title()
            known_face_identities.append(identity_name)
            print(f"[+] Registered Identity: {identity_name}")
        else:
            print(f"[x] Could not find a face in {filename}, skipping.")

print(f"[-] Database loaded. {len(known_face_identities)} identities registered.\n")

# --- STEP 2: LIVE VIDEO CAPTURE & PROCESSING ---
# 0 represents the default system webcam. Swap with a video file path or RTSP stream URL if needed.
video_capture = cv2.VideoCapture(0)

# Variables for optimizing performance (processing every alternate frame)
process_this_frame = True

while True:
    # Grab a single frame from the live video stream
    ret, frame = video_capture.read()
    if not ret:
        print("[x] Failed to grab frame from camera stream.")
        break

    # Resize frame to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert image from BGR (OpenCV default) to RGB (face_recognition default)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        # Find all faces and their embeddings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_identities = []
        for face_encoding in face_encodings:
            # See if the face matches any registered digital identity
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown Profile"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_identities[best_match_index]

            face_identities.append(name)

    # Toggle frame processing to save CPU cycles
    process_this_frame = not process_this_frame

    # --- STEP 3: OVERLAY RESULTS ON LIVE VIDEO ---
    for (top, right, bottom, left), name in zip(face_locations, face_identities):
        # Scale back up face locations since we processed a 1/4 sized frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a bounding box around the detected face
        # Green box for known identities, Red for unknown profiles
        box_color = (0, 255, 0) if name != "Unknown Profile" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

        # Draw a label banner below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 10), font, 0.7, (255, 255, 255), 1)

    # Display the resulting live feed
    cv2.imshow('Live Public Mentions AI Identity System', frame)

    # Hit 'q' on the keyboard to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
