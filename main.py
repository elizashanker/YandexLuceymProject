import sys
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime

WIDTH = 1200
LENGTH = 1500
LOGIN_WIDTH = WIDTH // 3
LOGIN_LENGTH = LENGTH // 5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("1.ui", self)

        self.sizes = QImage("logo.jpg")
        self.label.resize(self.sizes.width(), self.sizes.height())
        print(self.sizes.width(), self.sizes.height())
        self.pixmap = QPixmap("logo.jpg")
        self.label.setPixmap(self.pixmap)

        self.specialist_button.clicked.connect(self.specialist_button_click)
        self.login_button.clicked.connect(self.login_button_click)

    def specialist_button_click(self):
        self.MR = MakeReception()
        self.MR.show()

    def login_button_click(self):
        password, ok_pressed = QInputDialog.getText(self, "Вход",
                                                    "Введите код доступа:")
        if ok_pressed and password == "admin":
            self.AW = AdminWindow()
            self.AW.show()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("AdminWindow.ui", self)
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        self.dl = []
        self.names_list.addItems([item[0] for item in cur.execute("SELECT name FROM doctors").fetchall()])
        self.new_button.clicked.connect(self.new_button_click)
        self.edit_button.clicked.connect(self.edit_button_click)
        self.names_list.currentItemChanged.connect(self.change_name_info)
        self.delete_button.clicked.connect(self.delete_button_click)
        self.date_add_button.clicked.connect(self.date_add_button_click)
        self.date_delete_button.clicked.connect(self.date_delete_button_click)
        self.clean_button.clicked.connect(self.clean_all)
        self.comboBox.currentTextChanged.connect(self.change_date_info)
        self.photo_button.clicked.connect(self.photo_button_click)
        self.text_button.clicked.connect(self.text_button_click)

    def clean_all(self):
        self.name_line.setText("")
        self.prof_line.setText("")
        self.education_line.setText("")
        self.experiense_line.setText("")
        if self.dates_list.count() != 0:
            self.dates_list.clear()
        if self.comboBox.count() != 1:
            self.comboBox.clear()
            self.comboBox.addItem("Выбрать")

    # self.setGeometry(300, 100, 650, 450)
    # self.setWindowTitle('Пример работы с QtSql')
    def change_name_info(self):
        self.clean_all()
        if self.names_list.currentItem().text() != "Выбрать":
            self.con = sqlite3.connect("clinic.sqlite")
            cur = self.con.cursor()
            name = self.names_list.currentItem().text()
            result = cur.execute("SELECT name, prof, education, experience FROM doctors "
                                "WHERE name = '{}'".format(name)).fetchall()
            self.name_line.setText(result[0][0])
            self.prof_line.setText(result[0][1])
            self.education_line.setText(result[0][2])
            self.experiense_line.setText(result[0][3])

            self.id = cur.execute("SELECT id FROM doctors "
                            "WHERE name = '{}'".format(name)).fetchall()[0][0]

            request = cur.execute("SELECT title FROM dates "
                                "WHERE doctor_id = {}".format(self.id)).fetchall()
            a = self.dates_list.clear()
            if len(request) != 0:
                self.dates_list.addItems([item[0] for item in request])

            self.comboBox.addItems([item[0] for item in cur.execute("SELECT title FROM dates "
                                                                "WHERE taken = 1 and doctor_id = {}".format(self.id)).fetchall()])

    # Если картинки нет, то QPixmap будет пустым,
    # а исключения не будет
    # Отображаем содержимое QPixmap в объекте QLabel

    def new_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        name = self.name_line.text()
        flag = len(cur.execute("SELECT id FROM doctors "
                               "WHERE name = '{}'".format(name)).fetchall()) == 0
        if not (name.replace(" ", "") == "") and flag:
            add_text = ("INSERT INTO doctors (name, prof, education, experience) "
                        "VALUES ('{}', '{}', '{}', '{}')".format(name, self.prof_line.text(),
                                                                 self.education_line.text(),
                                                                 self.experiense_line.text()))
            count = cur.execute(add_text)
            self.con.commit()
            for x in self.dl:
                add_text = ("INSERT INTO dates (title, doctor_id) "
                            "VALUES ('{}', '{}')".format(x, self.id))
                count = cur.execute(add_text)
                self.con.commit()
            cur.close()
            self.names_list.addItem(name)
            self.clean_all()
        elif not flag:
            QMessageBox.critical(self, "Ошибка ", "Специалист с таким именем уже существует", QMessageBox.Ok)

    # self.names_list.setCurrentItem(self.name_list.currentItem())

    def edit_button_click(self):
        if self.names_list.currentItem().text() != "Выбрать":
            self.con = sqlite3.connect("clinic.sqlite")
            name = self.name_line.text()
            cur = self.con.cursor()
            result = cur.execute("UPDATE doctors "
                             "SET name = '{}',prof = '{}', education = '{}', experience = '{}' "
                             "WHERE name = '{}'".format(name,
                                                        self.prof_line.text(),
                                                        self.education_line.text(),
                                                        self.experiense_line.text(),
                                                        self.names_list.currentItem().text())).fetchall()
            self.con.commit()
            cur.close()
            self.names_list.currentItem().setText(name)

    def delete_button_click(self):
        if self.names_list.currentItem().text() != "Выбрать":
            self.con = sqlite3.connect("clinic.sqlite")
            cur = self.con.cursor()
            name = self.names_list.currentItem().text()
            if name.replace(" ", "") != "":
                result1 = cur.execute("DELETE from doctors WHERE name = '{}'".format(name)).fetchall()
                self.con.commit()
                result2 = cur.execute("DELETE from dates WHERE doctor_id = '{}'".format(self.id)).fetchall()
                self.con.commit()
                a = cur.execute("SELECT id FROM dates WHERE doctor_id = {}".format(self.id)).fetchall()
                #result3 = cur.execute("DELETE from clients "
                #                  "WHERE date_id IN (SELECT id FROM dates "
                #                  "WHERE doctor_id = {})".format(self.id)).fetchall()
                self.con.commit()
                print(а)
                cur.close()
                self.names_list.currentItem().setHidden(True)
                self.clean_all()

    def change_date_info(self):
        try:
            if self.comboBox.currentText() == "Выбрать":
                self.label_5.setText("ФИО: ")
                self.label_6.setText("Дата рождения: ")
                self.label_7.setText("Цель приема: ")
            else:
                cur = self.con.cursor()
                date_id = cur.execute("SELECT id FROM dates "
                                      "WHERE title = '{}'".format(self.comboBox.currentText())).fetchall()
                request = cur.execute("SELECT name, birthday, goal FROM clients "
                                      "WHERE date_id = {}".format(date_id[0][0])).fetchall()
                name = request[0][0]
                birthday = request[0][1]
                goal = request[0][2]
                self.label_5.setText("ФИО: " + name)
                self.label_6.setText("Дата рождения: " + birthday)
                self.label_7.setText("Цель приема: " + goal)
        except Exception as ex:
            pass

    def date_add_button_click(self):
        if self.names_list.currentItem().text() != "Выбрать":
            cur = self.con.cursor()
            request = ("INSERT INTO dates (title, doctor_id) "
                   "VALUES ('{}', '{}')".format(self.date_choose.text(), self.id))
            result = cur.execute(request).fetchall()
            self.con.commit()
            cur.close()
            self.dates_list.addItem(self.date_choose.text())

    def date_delete_button_click(self):
        if self.names_list.currentItem().text() != "Выбрать":
            self.con = sqlite3.connect("clinic.sqlite")
            cur = self.con.cursor()
            cur_item = self.dates_list.currentItem().text()
            if cur_item.replace(" ", "") != "":
                request = "DELETE from dates WHERE title = '{}'".format(self.dates_list.currentItem().text())
                result = cur.execute(request).fetchall()
                self.con.commit()
                cur.close()
                self.dates_list.currentItem().setHidden(True)

    def photo_button_click(self):
        if self.comboBox.currentText() != "Выбрать":
            cur = self.con.cursor()
            photoname = cur.execute("SELECT photo FROM clients "
                                    "WHERE date_id = (SELECT id FROM dates "
                                    "WHERE title = '{}')".format(self.comboBox.currentText())).fetchall()[0][0]
            self.PS = Photo(photoname)
            self.PS.show()
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы не выбрали приём", QMessageBox.Ok)

    def text_button_click(self):
        if self.comboBox.currentText() != "Выбрать":
            cur = self.con.cursor()
            textname = cur.execute("SELECT text FROM clients "
                                   "WHERE date_id = (SELECT id FROM dates "
                                   "WHERE title = '{}')".format(self.comboBox.currentText())).fetchall()[0][0]
            self.TS = Text(textname)
            self.TS.show()
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы не выбрали приём", QMessageBox.Ok)


class MakeReception(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MakeReception.ui", self)
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        self.names_list.addItems([item[0] for item in cur.execute("SELECT name FROM doctors").fetchall()])
        self.photoname = None
        self.textname = None

        self.names_list.currentItemChanged.connect(self.change_info)
        self.make_button.clicked.connect(self.make_button_click)
        self.photo_button.clicked.connect(self.photo_button_click)
        self.text_button.clicked.connect(self.text_button_click)

    def initUI(self):
        pass

    def change_info(self):
        name = self.names_list.currentItem().text()
        cur = self.con.cursor()
        request = cur.execute("SELECT id, prof, education, experience FROM doctors "
                              "WHERE name = '{}'".format(name)).fetchall()
        id = request[0][0]
        prof = request[0][1]
        education = request[0][2]
        experience = request[0][3]

        self.label.setText("Имя: " + name)
        self.prof_label.setText("Специальность: " + prof)
        self.education_label.setText("Образование: " + education)
        self.experience_label.setText("Опыт работы: " + experience)

        self.dates_list.clear()

        self.dates_list.addItems([item[0] for item in cur.execute("SELECT title FROM dates "
                                                                  "WHERE doctor_id = {} and taken = 0".format(
            id)).fetchall()])
        self.photoname = None
        self.textname = None

    def make_button_click(self):
        if self.dates_list.currentItem() is not None:
            cur = self.con.cursor()
            date_id = cur.execute("SELECT id FROM dates "
                                  "WHERE title = '{}'".format(self.dates_list.currentItem().text())).fetchall()
            print(date_id)
            add_text = ("INSERT INTO clients (name, birthday, goal, photo, text, date_id) "
                        "VALUES ('{}', '{}', '{}', '{}', '{}', {})".format(self.name_label.text(),
                                                                           self.birthday_label.text(),
                                                                           self.goal_label.text(), self.photoname,
                                                                           self.textname, date_id[0][0]))
            res = cur.execute(add_text).fetchall()
            self.con.commit()
            res = cur.execute("UPDATE dates "
                              "SET taken = 1 "
                              "WHERE id = '{}'".format(date_id[0][0])).fetchall()
            self.con.commit()
            QMessageBox.information(self, "Вы записаны", "Вы записались")
            self.photoname = None
            self.textname = None
            self.close()

    def photo_button_click(self):
        self.photoname = QFileDialog.getOpenFileName(
            self, "Выбрать картинку", "",
            "Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)")[0]

    def text_button_click(self):
        self.textname = QFileDialog.getOpenFileName(
            self, "Выбрать текстовый файл", "",
            "Текст (*.txt);;Все файлы (*)")[0]


class Photo(QWidget):
    def __init__(self, photoname):
        self.photoname = photoname
        super().__init__()
        self.initUI()

    def initUI(self):
        if self.photoname is not None and self.photoname != "None":
            self.sizes = QImage(self.photoname)
            self.setGeometry(400, 400, self.sizes.width(), self.sizes.height())
            self.setWindowTitle("Результаты анализов")
            self.image = QLabel(self)
            self.pixmap = QPixmap(self.photoname)
            self.image.setPixmap(self.pixmap)
        else:
            print(self.photoname)
            QMessageBox.information(self, "Нет файла", "Пользователь не приложил результаты анализов", QMessageBox.Ok)


class Text(QWidget):
    def __init__(self, textname):
        self.textname = textname
        super().__init__()
        self.initUI()

    def initUI(self):
        if self.textname is not None and self.textname != "None":
            print(self.textname)
            self.setGeometry(0, 0, WIDTH, LENGTH)
            self.setWindowTitle("Заключение врача")
            self.text = QLabel(self)
            self.text.resize(WIDTH, LENGTH)
            with open(self.textname, encoding="utf-8") as f:
                text = f.read()
                self.text.setText(text)
        else:
            QMessageBox.information(self, "Нет файла", "Пользователь не приложил заключение", QMessageBox.Ok)
