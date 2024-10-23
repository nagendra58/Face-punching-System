from flask import Flask, render_template, Response, redirect, url_for
import cv2
import face_recognition
import numpy as np
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Load known faces and names
known_faces = []
known_names = []
attendance_log = {}

def load_known_faces(known_faces_directory):
    for filename in os.listdir(known_faces_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(known_faces_directory, filename))
            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(face_encoding)
            known_names.append(os.path.splitext(filename)[0])

load_known_faces('employee_faces')

def log_attendance(employee_id, name, status):
    try:
        df = pd.read_csv("attendance.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Employee Name", "Date", "Time", "Status"])

    now = datetime.now()
    new_row = {
        "ID": employee_id,
        "Employee Name": name,
        "Date": now.strftime('%Y-%m-%d'),
        "Time": now.strftime('%H:%M:%S'),
        "Status": status
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("attendance.csv", index=False)

def check_for_face(frame):
    rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_small_frame)
    if face_encodings:
        return face_encodings[0]  # Return the first detected face encoding
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Encode the frame
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/checkin')
def check_in():
    ret, frame = video_capture.read()
    if not ret:
        return redirect(url_for('index'))

    face_encoding = check_for_face(frame)
    if face_encoding is not None:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            employee_id = known_names[first_match_index].split('_')[0]
            now = datetime.now()
            if employee_id not in attendance_log or attendance_log[employee_id].get("check_in") is None:
                log_attendance(employee_id, known_names[first_match_index], status="Check-in")
                attendance_log[employee_id] = {"check_in": now, "check_out": None}

    return redirect(url_for('index'))

@app.route('/checkout')
def check_out():
    ret, frame = video_capture.read()
    if not ret:
        return redirect(url_for('index'))

    face_encoding = check_for_face(frame)
    if face_encoding is not None:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            employee_id = known_names[first_match_index].split('_')[0]
            now = datetime.now()
            if employee_id in attendance_log and attendance_log[employee_id].get("check_out") is None:
                log_attendance(employee_id, known_names[first_match_index], status="Check-out")
                attendance_log[employee_id]["check_out"] = now

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
