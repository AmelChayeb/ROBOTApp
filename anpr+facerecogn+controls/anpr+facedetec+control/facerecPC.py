import cv2
import os
import sys
import pytesseract
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from dash1 import Ui_Dash
import sqlite3
import conexionBD
from Levenshtein import distance
import numpy as np
import face_recognition

class Dash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dash()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(0)

        self.timer = QtCore.QTimer(self)
        self.timer.start(50)
        self.ui.bt_match.clicked.connect(self.on_bt_match_clicked)

        self.datosTotal = conexionBD.Registro_datos()
        # Connect to the SQLite database
        self.conn = sqlite3.connect('base_datos.db')
        self.c = self.conn.cursor()

        # Load the known faces and their employee IDs from the database
        self.known_faces = []
        self.known_ids = []
        for row in self.c.execute("SELECT AVATAR, EMPLOYEEID FROM tabla_datos"):
            # Load the image from the database
            image_data = row[0]
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Compute the face encoding and add it to the known faces list
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_faces.append(face_encoding)

            # Add the employee ID to the known IDs list
            self.known_ids.append(row[1])

        # Initialize the video capture object
        self.video_capture = cv2.VideoCapture(0)

        # Set up a timer to read the video stream and display it in the imgLabel QLabel
        self.ui.bt_face.clicked.connect(self.on_bt_face_clicked)

    def on_bt_face_clicked(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def on_bt_match_clicked(self):
        text = "YES"
        self.ui.frame.setText(text)

    def display_video_stream(self):
        # Capture a single frame from the camera
        ret, frame = self.video_capture.read()

        # Find all the faces and their encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop over each face found in the frame
        for face_encoding in face_encodings:
            # Check if any face was found
            matches = face_recognition.compare_faces(self.known_faces, face_encoding)
            first_name = "Unknown"

            # If a match was found, use the ID of the first match
            if True in matches:
                first_match_index = matches.index(True)
                employee_id = self.known_ids[first_match_index]

                # Get the corresponding employee data from the database
                self.c.execute("SELECT FIRSTNAME, LASTNAME, AVATAR FROM tabla_datos WHERE EMPLOYEEID=?", (employee_id,))
                employee_data = self.c.fetchone()

                # Update the UI with the employee data
                if employee_data:
                    first_name = employee_data[0]
                    last_name = employee_data[1]
                    avatar_data = employee_data[2]

                    # Display the employee's avatar in the frameF QLabel
                    avatar_image = QtGui.QPixmap()
                    avatar_image.loadFromData(avatar_data)
                    self.ui.frameF.setPixmap(avatar_image)

                    # Update the employee's first name in the firstname QLabel
                    self.ui.employeeid.setText(employee_id)
                    self.ui.firstname.setText(first_name)
                    self.ui.lastname.setText(last_name)

            # Draw a box around the face and label it with the person's ID
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, str(first_name), (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255),
                        2)

        # Resize the frame to 800x500
        frame_resized = cv2.resize(frame, (800, 500))

        # Convert the frame from BGR to RGB color
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # Create a QImage from the frame data
        image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)
        # Set the pixmap to the imgLabel QLabel
        self.ui.imgLabel.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dash()
    dashboard.show()
    sys.exit(app.exec_())
