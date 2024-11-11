import cv2
import face_recognition
import pickle
import os
import numpy as np

def collect_face():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Create directory if it doesn't exist
    if not os.path.exists('face_data'):
        os.makedirs('face_data')

    student_name = input("Enter student name: ")
    student_id = input("Enter student ID: ")

    face_encodings = []

    print("Press 'c' to capture face or 'q' to quit")

    while True:
        ret, frame = cap.read()

        # Find faces in frame
        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Collect Faces', frame)

        key = cv2.waitKey(1)
        if key == ord('c'):
            # Get face encoding
            face_encoding = face_recognition.face_encodings(frame, face_locations)
            if face_encoding:
                face_encodings.append({
                    'name': student_name,
                    'id': student_id,
                    'encoding': face_encoding[0]
                })
                print(f"Face captured for {student_name}")
                break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save face encodings
    if face_encodings:
        with open('face_data/encodings.pkl', 'ab') as f:
            pickle.dump(face_encodings, f)
        print("Face data saved successfully!")

if __name__ == "__main__":
    collect_face()