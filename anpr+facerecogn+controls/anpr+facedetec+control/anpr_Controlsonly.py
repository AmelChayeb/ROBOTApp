import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QDate, QTimer, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
import socket
from dash import Ui_Dash
import sys
import conexionBD


from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import sqlite3
from dash import Ui_Dash


# Define server IP address and port number
SERVER_IP = '192.168.1.121'
SERVER_PORT = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Define key bindings for sending commands
key_commands = {
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
def send_command( command):
    client_socket.send(command.encode())
    response = client_socket.recv(1024).decode()
    print(response)

class DashDialog(QDialog, Ui_Dash):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # create a QTimer object to update the date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

    def update_date_time(self):
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        # remote code for keypress

    def keyPressEvent(self, event: QKeyEvent):
        # Check if the key pressed is a mecanum wheel control key
        if event.key() in key_commands and not event.isAutoRepeat():
            command = key_commands[event.key()]
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
                button = self.bt_5
            elif command == "rotate_right":
                button = self.bt_0

            # Change the color of the button
            button.setStyleSheet('background-color:rgb(221, 165, 51) ;')
            # Send the command
            send_command(command)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        # Check if the key released is a mecanum wheel control key
        if event.key() in key_commands and not event.isAutoRepeat():
            # Find the corresponding button for the command
            command = key_commands[event.key()]
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
                button = self.bt_5
            elif command == "rotate_right":
                button = self.bt_0
            # Change the color of the button back to white
            button.setStyleSheet('background-color: rgb(14, 131, 136);')
            send_command("Stop")
        else:
            super().keyReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DashDialog()
    dialog.show()

    sys.exit(app.exec_())
