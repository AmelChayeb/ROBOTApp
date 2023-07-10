from PyQt5.QtCore import pyqtSignal
import datetime
import sys
import socket
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog
from Qt import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QDateTime, QDate, QTimer

from homepage1 import Ui_MainWindow

from dash import Ui_Dash

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
from PyQt5.QtWidgets import QFileDialog



class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        # Connect the "Start" button to the function that connects to the server and shows the dashboard
        self.start_bt.clicked.connect(self.connect_and_show_dashboard)

    def connect_and_show_dashboard(self):
        try:
            # Connect to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostname(), 1234))

            # Show success message
            QtWidgets.QMessageBox.information(self, "Connection Status", "Connected to server.")

            # Close the current window
            self.close()

            # Show the dashboard
            dash = DashDialog(s)
            # uidash = Ui_Dash()
            # uidash.setupUi(dash)
            dash.setWindowFlags(dash.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
            dash.exec_()

        except Exception as e:
            # Show error message
            QtWidgets.QMessageBox.warning(self, "Connection Status", f"Failed to connect to server.\n{e}")



class DashDialog(QDialog, Ui_Dash):

    def __init__(self,socket):
        super().__init__()
        self.setupUi(self)


        self.client_socket = socket
        # Define server IP address and port number
        self.SERVER_IP = '192.168.1.23'
        self.SERVER_PORT = 9999
        # create a QTimer object to update the date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)  # update every 1000 milliseconds (i.e. 1 second)
        # Define key bindings for sending commands
        self.key_commands = {
            Qt.Key_8: 'forward',
            Qt.Key_2: 'backward',
            Qt.Key_4: 'left',
            Qt.Key_6: 'right',
            Qt.Key_7: 'diagonal_forward_left',
            Qt.Key_9: 'diagonal_forward_right',
            Qt.Key_1: 'diagonal_backward_left',
            Qt.Key_3: 'diagonal_backward_right',
            Qt.Key_0: 'rotate_left',
            Qt.Key_5: 'rotate_right'
        }



    def update_date_time(self):
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)



    def send_command(self, command):
        self.client_socket.send(command.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    # remote code for keypress
    def keyPressEvent(self, event: QKeyEvent):
        # Check if the key pressed is a mecanum wheel control key
        if event.key() in self.key_commands and not event.isAutoRepeat():
            command = self.key_commands[event.key()]
            # Find the corresponding button for the command
            if command == "forward":
                button = self.bt_8
            elif command == "left":
                button = self.bt_4
            elif command == "right":
                button = self.bt_6
            elif command == "backward":
                button = self.bt_2
            elif command == "diagonal_forward_left":
                button = self.bt_7
            elif command == "diagonal_forward_right":
                button = self.bt_9
            elif command == "diagonal_backward_left":
                button = self.bt_1
            elif command == "diagonal_backward_right":
                button = self.bt_3
            elif command == "rotate_left":
                button = self.bt_0
            elif command == "rotate_right":
                button = self.bt_0

            # Change the color of the button yellow
            button.setStyleSheet('background-color:  rgb(221, 165, 51);')
            # Send the command
            self.send_command(command)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        # Check if the key released is a mecanum wheel control key
        if event.key() in self.key_commands and not event.isAutoRepeat():
            # Find the corresponding button for the command
            command = self.key_commands[event.key()]
            if command == "forward":
                button = self.bt_8
            elif command == "left":
                button = self.bt_4
            elif command == "right":
                button = self.bt_6
            elif command == "backward":
                button = self.bt_2
            elif command == "diagonal_forward_left":
                button = self.bt_7
            elif command == "diagonal_forward_right":
                button = self.bt_9
            elif command == "diagonal_backward_left":
                button = self.bt_1
            elif command == "diagonal_backward_right":
                button = self.bt_3
            elif command == "rotate_left":
                button = self.bt_0
            elif command == "rotate_right":
                button = self.bt_0

            # Change the color of the button back to recent color
            button.setStyleSheet('background-color:  rgb(14, 131, 136);')
            self.send_command("Stop")
        else:
            super().keyReleaseEvent(event)






app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
dialog = DashDialog(socket)



sys.exit(app.exec_())

