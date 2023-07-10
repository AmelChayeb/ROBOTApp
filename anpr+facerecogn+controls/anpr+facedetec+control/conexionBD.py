import sqlite3

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap


class Registro_datos():
    def __init__(self):
        self.conexion = sqlite3.connect('base_datos.db')

    def insert_employee(self,blob_data, employeeid, firstname, lastname, gender, licensenumberplate, departmentid ,email, phone,doe):

        cur = self.conexion.cursor()
        sql = '''INSERT INTO tabla_datos (AVATAR,EMPLOYEEID, FIRSTNAME, LASTNAME, GENDER, LICENSENUMBERPLATE, DEPARTMENTID, EMAIL, PHONE, DOE) VALUES(:blob_data, :employeeid, :firstname, :lastname, :gender, :licensenumberplate, :departmentid, :email, :phone, :doe)'''
        cur.execute(sql,
                    {'blob_data': blob_data, 'employeeid': employeeid, 'firstname': firstname, 'lastname': lastname,
                     'gender': gender, 'licensenumberplate': licensenumberplate, 'departmentid': departmentid,
                     'email': email, 'phone': phone, 'doe': doe})


        self.conexion.commit()
        cur.close()

    def find_employees(self):
        cursor = self.conexion.cursor()
        sql = 'SELECT * FROM tabla_datos '
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        results = []
        for row in registro:
            avatar_bytes = row[1]  # assuming the avatar column is the first column
            avatar_pixmap = QPixmap()
            avatar_pixmap.loadFromData(avatar_bytes)
            size = QtCore.QSize(150, 150)  # set the desired size
            resized_pixmap = avatar_pixmap.scaled(size,
                                                  QtCore.Qt.KeepAspectRatio)  # scale the pixmap to the desired size

            results.append((*row[:1], resized_pixmap, *row[2:]))

        return results

    def find_employee(self, nombre_producto):
        cur = self.conexion.cursor()
        sql = '''SELECT * FROM tabla_datos WHERE FIRSTNAME = {}'''.format(nombre_producto)
        cur.execute(sql)
        registro = cur.fetchall()
        cur.close()
        results = []
        for row in registro:
            avatar_bytes = row[1]  # assuming the avatar column is the first column
            avatar_pixmap = QPixmap()
            avatar_pixmap.loadFromData(avatar_bytes)
            size = QtCore.QSize(150, 150)  # set the desired size
            resized_pixmap = avatar_pixmap.scaled(size,
                                                  QtCore.Qt.KeepAspectRatio)  # scale the pixmap to the desired size

            results.append((*row[:1], resized_pixmap, *row[2:]))

        return results

    def erase_employee(self, nombre):
        cur = self.conexion.cursor()
        sql = '''DELETE FROM tabla_datos WHERE FIRSTNAME = {}'''.format(nombre)
        cur.execute(sql)
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def update_employee(self,employeeid, firstname,  lastname, gender,licensenumberplate, departmentid, email, phone, doe):
        cur = self.conexion.cursor()
        sql = '''UPDATE tabla_datos SET  FIRSTNAME = '{}', LASTNAME = '{}', GENDER = '{}',LICENSENUMBERPLATE = '{}', DEPARTMENTID = '{}', EMAIL= '{}', PHONE= '{}', DOE= '{}' WHERE EMPLOYEEID = '{}' '''.format(firstname, lastname, gender, licensenumberplate, departmentid, email, phone , doe, employeeid)
        cur.execute(sql)
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act
