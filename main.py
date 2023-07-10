# @autor: Magno Efren
# https://www.youtube.com/c/MagnoEfren
import sys

from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap

import conexionBD
from GUI import *

from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import sqlite3

class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)




        self.datosTotal = conexionBD.Registro_datos()
        self.ui.bt_refresh.clicked.connect(self.allEmployee)
        self.ui.bt_add.clicked.connect(self.addEmployee)
        self.ui.bt_search.clicked.connect(self.searchEmployee)
        self.ui.bt_erase.clicked.connect(self.eraseEmployee)
        self.ui.bt_update.clicked.connect(self.updateEmployee)
        self.ui.readBtn_2.clicked.connect(self.load_image)


        self.ui.table_employees.setColumnWidth(0, 150)
        self.ui.table_employees.setColumnWidth(1, 200)
        self.ui.table_employees.setColumnWidth(2, 200)
        self.ui.table_employees.setColumnWidth(3, 200)
        self.ui.table_employees.setColumnWidth(4, 200)
        self.ui.table_employees.setColumnWidth(5, 200)
        self.ui.table_employees.setColumnWidth(6, 200)
        self.ui.table_employees.setColumnWidth(7, 200)
        self.ui.table_employees.setColumnWidth(8, 200)
        self.ui.table_employees.setColumnWidth(9, 200)


        self.ui.table_erasing.setColumnWidth(0, 200)
        self.ui.table_erasing.setColumnWidth(1, 200)
        self.ui.table_erasing.setColumnWidth(2, 200)
        self.ui.table_erasing.setColumnWidth(3, 200)
        self.ui.table_erasing.setColumnWidth(4, 200)
        self.ui.table_erasing.setColumnWidth(5, 200)
        self.ui.table_erasing.setColumnWidth(6, 200)
        self.ui.table_erasing.setColumnWidth(7, 200)
        self.ui.table_erasing.setColumnWidth(8, 200)
        self.ui.table_erasing.setColumnWidth(9, 200)


        self.ui.table_searching.setColumnWidth(0, 200)
        self.ui.table_searching.setColumnWidth(1, 200)
        self.ui.table_searching.setColumnWidth(2, 200)
        self.ui.table_searching.setColumnWidth(3, 200)
        self.ui.table_searching.setColumnWidth(4, 200)
        self.ui.table_searching.setColumnWidth(5, 200)
        self.ui.table_searching.setColumnWidth(6, 200)
        self.ui.table_searching.setColumnWidth(7, 200)
        self.ui.table_searching.setColumnWidth(8, 200)
        self.ui.table_searching.setColumnWidth(9, 200)

    def allEmployee(self):
        datos = self.datosTotal.find_employees()
        i = len(datos)

        self.ui.table_employees.setRowCount(i)
        tablerow = 0
        for row in datos:
            for column_number, column_data in enumerate(row):
                if column_number == 0:
                    continue  # Skip the first column
                elif column_number == 1:
                    #item = self.getImageLabel(column_data)
                    #self.ui.table_employees.setCellWidget(tablerow, 0, item)

                    # Create a QTableWidgetItem with an empty text
                    item = QtWidgets.QTableWidgetItem('')
                    # Set the pixmap as the background of the item
                    item.setBackground(QtGui.QBrush(column_data))
                    self.ui.table_employees.setItem(tablerow, column_number - 1, item)
                else:
                    item = QtWidgets.QTableWidgetItem(str(column_data))
                    self.ui.table_employees.setItem(tablerow, column_number - 1, item)
            tablerow += 1

        self.ui.table_employees.verticalHeader().setDefaultSectionSize(100)
    def getImageLabel(self,image):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image,'jpg')
        imageLabel.setPixmap(pixmap)
        return imageLabel

    def addEmployee(self):
        avatar = self.ui.image.pixmap()
        employeeid = self.ui.employeeidA.text()
        firstname = self.ui.firstnameA.text()
        lastname = self.ui.lastnameA.text()
        gender = self.ui.genderA.text()
        licensenumberplate = self.ui.licensenumberplateA.text()
        departmentid = self.ui.departmentidA.text()
        email = self.ui.emailA.text()
        phone = self.ui.phoneA.text()
        doe = self.ui.doeA.text()
        # Check if any of the required fields are empty
        if not all([firstname, lastname, gender, licensenumberplate, departmentid, email, phone, doe]):
            self.ui.borrar_ok_2.setText("ERROR: Please fill in all required fields.")
            return

        if avatar is not None :
            byte_array  = QByteArray()# create a QByteArray object to hold the binary data
            buffer = QBuffer(byte_array) # create a QBuffer object to write binary data to the QByteArray
            buffer.open(QIODevice.WriteOnly)# open the buffer for writing
            avatar.toImage().save(buffer, "PNG")# save the pixmap as a PNG image to the buffer
            blob_data = bytes(byte_array)  # convert the QByteArray to bytes

        self.datosTotal.insert_employee(blob_data,employeeid, firstname, lastname, gender,licensenumberplate, departmentid, email, phone, doe)


        self.ui.employeeidA.clear()
        self.ui.firstnameA.clear()
        self.ui.lastnameA.clear()
        self.ui.genderA.clear()
        self.ui.licensenumberplateA.clear()
        self.ui.departmentidA.clear()
        self.ui.emailA.clear()
        self.ui.phoneA.clear()
        self.ui.doeA.clear()
        self.ui.borrar_ok_2.setText("EMPLOYEE ADDED")
    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            ".",
            "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            pixmap = QPixmap(filename)
            pixmap = pixmap.scaledToWidth(self.ui.image.width(), Qt.SmoothTransformation)
            self.ui.image.setPixmap(pixmap)

    def updateEmployee(self):
        id_producto = self.ui.id_producto.text()
        id_producto = str("'" + id_producto + "'")
        nombreXX = self.datosTotal.find_employee(id_producto)

        if nombreXX != None:
            self.ui.id_buscar.setText("UPDATE")
            employeeidM = self.ui.employeeidUP.text()
            firstnameM = self.ui.firstnameUP.text()
            lastnameM = self.ui.lastnameUP.text()
            genderM = self.ui.genderUP.text()
            licensenumberplateM = self.ui.licensenumberplateUP.text()
            departmentidM = self.ui.departmentidUP.text()
            emailM = self.ui.emailUP.text()
            phoneM = self.ui.phoneUP.text()
            doeM = self.ui.doeUP.text()
            act = self.datosTotal.update_employee(employeeidM, firstnameM, lastnameM, genderM, licensenumberplateM, departmentidM, emailM, phoneM, doeM)
            if act == 1:
                self.ui.id_buscar.setText("UPDATED")
                self.ui.employeeidUP.clear()
                self.ui.firstnameUP.clear()
                self.ui.lastnameUP.clear()
                self.ui.genderUP.clear()
                self.ui.licensenumberplateUP.clear()
                self.ui.departmentidUP.clear()
                self.ui.id_producto.clear()
                self.ui.emailUP.clear()
                self.ui.phoneUP.clear()
                self.ui.doeUP.clear()
            elif act == 0:
                self.ui.id_buscar.setText("ERROR")
                self.ui.employeeidUP.clear()
                self.ui.firstnameUP.clear()
                self.ui.lastnameUP.clear()
                self.ui.genderUP.clear()
                self.ui.licensenumberplateUP.clear()
                self.ui.departmentidUP.clear()
                self.ui.id_producto.clear()
                self.ui.emailUP.clear()
                self.ui.phoneUP.clear()
                self.ui.doeUP.clear()
            else:
                self.ui.id_buscar.setText("INCORRECT")
        else:
            self.ui.id_buscar.setText("NOT FOUND")

    def searchEmployee(self):
        nombre_producto = self.ui.firstnameB.text()
        nombre_producto = str("'" + nombre_producto + "'")

        datosB = self.datosTotal.find_employee(nombre_producto)

        i = len(datosB)
        self.ui.table_searching.setRowCount(i)
        tablerow = 0

        for row in datosB:
            for column_number, column_data in enumerate(row):
                if column_number == 0:
                    continue  # Skip the first column
                elif column_number == 1:
                    #item = self.getImageLabel(column_data)
                    #self.ui.table_searching.setCellWidget(tablerow, 0, item)

                    # Create a QTableWidgetItem with an empty text
                    item = QtWidgets.QTableWidgetItem('')
                    # Set the pixmap as the background of the item
                    item.setBackground(QtGui.QBrush(column_data))
                    self.ui.table_searching.setItem(tablerow, column_number - 1, item)

                else:
                    item = QtWidgets.QTableWidgetItem(str(column_data))
                    self.ui.table_searching.setItem(tablerow, column_number - 1, item)
            tablerow += 1

        self.ui.table_searching.verticalHeader().setDefaultSectionSize(150)



    def eraseEmployee(self):
        eliminar = self.ui.firstname_erase.text()
        eliminar = str("'" + eliminar + "'")
        resp = (self.datosTotal.erase_employee(eliminar))
        datos = self.datosTotal.find_employees()
        i = len(datos)
        self.ui.table_erasing.setRowCount(i)
        tablerow = 0
        for row in datos:
            for column_number, column_data in enumerate(row):
                if column_number == 0:
                    continue  # Skip the first column
                elif column_number == 1:
                    # item = self.getImageLabel(column_data)
                    # self.ui.table_searching.setCellWidget(tablerow, 0, item)

                    # Create a QTableWidgetItem with an empty text
                    item = QtWidgets.QTableWidgetItem('')
                    # Set the pixmap as the background of the item
                    item.setBackground(QtGui.QBrush(column_data))
                    self.ui.table_erasing.setItem(tablerow, column_number - 1, item)

                else:
                    item = QtWidgets.QTableWidgetItem(str(column_data))
                    self.ui.table_erasing.setItem(tablerow, column_number - 1, item)
            tablerow += 1
        self.ui.table_erasing.verticalHeader().setDefaultSectionSize(150)

        if resp is None or resp == 0:
            self.ui.borrar_ok.setText("NOT FOUND")
        else:
            self.ui.borrar_ok.setText("DELETED")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())
