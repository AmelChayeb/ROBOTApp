import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from dash import Ui_Dash

import socket
import cv2
import pickle
import struct
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class Dash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dash()
        self.ui.setupUi(self)

    def receive_video_from_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '192.168.1.23'
        port = 9999
        client_socket.connect((host_ip, port))
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    print("No data received from server")
                    break
                data += packet
                print(f"Received {len(packet)} bytes of data")

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            # Convert frame to QImage
            height, width, _ = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Convert QImage to QPixmap
            pixmap = QPixmap.fromImage(q_img)

            # Display the QPixmap in QLabel
            self.ui.imgLabel.setPixmap(pixmap.scaled(self.ui.imgLabel.width(), self.ui.imgLabel.height(), Qt.AspectRatioMode.KeepAspectRatio))

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        client_socket.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dash()
    dashboard.show()
    dashboard.receive_video_from_server()
    sys.exit(app.exec_())
