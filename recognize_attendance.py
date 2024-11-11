import cv2
import face_recognition
import pickle
import pandas as pd
from datetime import datetime
import numpy as np
import os

def load_known_faces():
    known_faces = []
    try:
        with open('face_data/encodings.pkl', 'rb') as f:
            while True:
                try:
                    known_faces.extend(pickle.load(f))
                except EOFError:
                    break
    except FileNotFoundError:
        print("No face data found!")
    return known_faces

def mark_attendance():
    # Load known faces
    known_faces = load_known_faces()
    if not known_faces:
        return

    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Create attendance directory if not exists
    if not os.path.exists('attendance'):
        os.makedirs('attendance')

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    attendance_file = f'attendance/{today}.csv'

    # Initialize or load attendance DataFrame
    if os.path.exists(attendance_file):
        df = pd.read_csv(attendance_file)
    else:
        df = pd.DataFrame(columns=['Student_ID', 'Name', 'Time'])

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()

        # Find faces in frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check each known face
            for known_face in known_faces:
                matches = face_recognition.compare_faces([known_face['encoding']], face_encoding)
                if matches[0]:
                    name = known_face['name']
                    student_id = known_face['id']

                    # Check if attendance already marked
                    if not ((df['Student_ID'] == student_id) & (df['Name'] == name)).any():
                        current_time = datetime.now().strftime('%H:%M:%S')
                        df = pd.concat([df, pd.DataFrame({
                            'Student_ID': [student_id],
                            'Name': [name],
                            'Time': [current_time]
                        })], ignore_index=True)
                        print(f"Attendance marked for {name}")

                    # Draw rectangle around face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Mark Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save attendance
    df.to_csv(attendance_file, index=False)
    print(f"Attendance saved to {attendance_file}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mark_attendance()