import cv2
import os
import pytesseract
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from dash import Ui_Dash
import sqlite3
import conexionBD
from Levenshtein import distance

class Dash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dash()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(0)
        self.plate_cascade = cv2.CascadeClassifier("C:\haarcascade_russian_plate_number.xml")
        self.min_area = 500
        self.count = 0

        self.plates_images = []

        self.last_anpr_result = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

        self.ui.bt_anpr.clicked.connect(self.on_bt_anpr_clicked)
        self.ui.bt_check.clicked.connect(self.on_bt_check_clicked)

        self.datosTotal = conexionBD.Registro_datos()




    def update_frame(self):

        # Capture frame from video
        ret, frame = self.cap.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect license plates using Haar Cascade classifier
        plates = self.plate_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around license plates and display frame in image label
        for (x, y, w, h) in plates:
            area = w * h
            if area > self.min_area:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, "NUMBER PLATE", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                plate_roi = gray[y:y + h, x:x + w]

                plate_text = pytesseract.image_to_string(plate_roi, lang='eng')
                print(f"Detected plate: {plate_text.strip()}")

                self.ui.lineEdit.setText(plate_text.strip())
                self.plates_images.append(plate_roi)
            # Capture license plate image and show in frameP QLabel
            plate_roi = cv2.resize(plate_roi, (150, 100))
            cv2.imwrite('license_plate.png', plate_roi)
            pixmap = QPixmap('license_plate.png')
            self.ui.frameP.setPixmap(pixmap)


        frame = cv2.resize(frame, (800, 500))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        q_pixmap = QtGui.QPixmap.fromImage(q_image)
        self.ui.imgLabel.setPixmap(q_pixmap)

    def check_license(self, license_number_plate):

            self.conexion = sqlite3.connect('base_datos.db')
            self.cur = self.conexion.cursor()
            # Execute SQL query to fetch license plate data
            sql = "SELECT * FROM tabla_datos WHERE LICENSENUMBERPLATE = ?"
            self.cur.execute(sql, (license_number_plate,))
            rows = self.cur.fetchall()

            if len(rows) >= 1:
                # If one or more rows are returned, the plate exists in the database
                self.ui.lineEdit.setText(license_number_plate)
                if self.last_anpr_result is not None:
                    # Check similarity between new and last result
                    dist = distance(license_number_plate, self.last_anpr_result)
                    if dist <= 1:
                        self.ui.statuslabel.setText("KNOWN")
                    else:
                        self.ui.statuslabel.setText("UNKNOWN")
                else:
                    self.ui.statuslabel.setText("UNKNOWN")
                self.last_anpr_result = license_number_plate
            else:

                self.ui.statuslabel.setText("No match")
                self.last_anpr_result = None

    def on_bt_check_clicked(self):
        license_number_plate = self.ui.lineEdit.text()
        self.check_license(license_number_plate)

    def on_bt_anpr_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(50)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dash()
    dashboard.show()
    sys.exit(app.exec_())
