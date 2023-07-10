import pickle
import socket
import struct

import cv2
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from dash import Ui_Dash
import sqlite3
import numpy as np
import face_recognition

class Dash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dash()
        self.ui.setupUi(self)

        # Set up a timer to update the video stream
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

        # Connect to the video stream server
        self.server_ip = '192.168.1.23'
        self.server_port = 9999
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

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

            try:
                face_encoding = face_recognition.face_encodings(image)[0]
            except IndexError as e:
                print(e)
                sys.exit(1)
            self.known_faces.append(face_encoding)

            # Add the employee ID to the known IDs list
            self.known_ids.append(row[1])

    def update_frame(self):
        frame_size_data = self.client_socket.recv(8)
        if not frame_size_data:
            return

        frame_size = struct.unpack("Q", frame_size_data)[0]

        if frame_size > 0:
            frame_data = b""
            while len(frame_data) < frame_size:
                remaining_bytes = frame_size - len(frame_data)
                chunk_size = min(4096, remaining_bytes)
                chunk = self.client_socket.recv(chunk_size)
                if not chunk:
                    break
                frame_data += chunk

            frame = pickle.loads(frame_data)
            processed_frame = self.display_video_stream(frame)
            self.display_frame(processed_frame)

    def display_video_stream(self, frame):
        # Convert the frame from BGR color to RGB color
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and their encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) > 0:
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

                        # Display the employee's avatar in the frame QLabel
                        avatar_image = QtGui.QPixmap()
                        avatar_image.loadFromData(avatar_data)
                        self.ui.frame.setPixmap(avatar_image)

                        # Update the employee's first name in the firstname QLabel
                        self.ui.employeeid.setText(employee_id)
                        self.ui.firstname.setText(first_name)
                        self.ui.lastname.setText(last_name)

                # Draw a box around the face and label it with the person's ID
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
                cv2.putText(frame, str(employee_id), (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255),
                            2)

        return frame

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_pixmap = QPixmap.fromImage(q_image)
        self.ui.imgLabel.setPixmap(q_pixmap.scaled(self.ui.imgLabel.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dash()
    dashboard.show()
    sys.exit(app.exec_())
