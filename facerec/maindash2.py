import cv2
import sys
import face_recognition
import cv2
import numpy as np
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import conexionBD
from dash import Ui_Dash
from PyQt5.QtGui import QKeyEvent
import socket
from PyQt5.QtCore import (QThread, Qt, pyqtSignal)



# Define server IP address and port number
SERVER_IP = '192.168.1.23'
SERVER_PORT = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))


class Dash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dash()
        self.ui.setupUi(self)

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

    def display_video_stream(self):
        # Capture a single frame from the camera
        ret, frame = self.video_capture.read()

        # Convert the frame from BGR color to RGB color
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and their encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop over each face found in the frame
        for face_encoding in face_encodings:
            # Check if any face was found
            matches = face_recognition.compare_faces(self.known_faces, face_encoding)
            employee_id = "Unknown"

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
            cv2.putText(frame, str(employee_id), (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255),
                        2)

        # Display the resulting image in the imgLabel QLabel
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        self.ui.imgLabel.setPixmap(QtGui.QPixmap.fromImage(p))




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dash()
    dashboard.show()
    sys.exit(app.exec_())
