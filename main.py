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
        self.specialist_button.clicked.connect(self.specialist_button_click)
        self.login_button.clicked.connect(self.login_button_click)

    def initUI(self):
        pass

    '''self.setGeometry(500, 500, WIDTH, LENGTH)
    self.setWindowTitle("Запись к врачу")

    # self.text_field = QTextEdit(self)
    # self.text_field.move(0, 100)

    self.specialist_button = QPushButton("Выбрать специалиста", self)
    self.specialist_button.resize(WIDTH // 3, LENGTH // 10)
    self.specialist_button.move(WIDTH // 3, LENGTH // 10)

    self.service_button = QPushButton("Выбрать категорию приема", self)
    self.service_button.resize(WIDTH // 3, LENGTH // 10)
    self.service_button.move(WIDTH // 3, 3 * (LENGTH // 10))

    self.date_button = QPushButton("Выбрать дату и время", self)
    self.date_button.resize(WIDTH // 3, LENGTH // 10)
    self.date_button.move(WIDTH // 3, 5 * (LENGTH // 10))

    self.login_button = QPushButton("Вход", self)
    self.login_button.resize(WIDTH // 3, LENGTH // 10)
    self.login_button.move(WIDTH // 3, 7 * (LENGTH // 10))'''

    def specialist_button_click(self):
        try:
            self.MR = MakeReception()
            self.MR.show()
        except Exception as ex:
            print(ex)

    def login_button_click(self):
        password, ok_pressed = QInputDialog.getText(self, "Вход",
                                                    "Введите код доступа:")
        if ok_pressed and password == "admin":
            self.AW = AdminWindow()
            self.AW.show()


'''
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, LOGIN_WIDTH, LOGIN_LENGTH)
        self.setWindowTitle("Вход")

        self.label = QLabel(self)
        self.label.setText("Введите код доступа:")
        self.label.move(LOGIN_WIDTH // 5, LOGIN_LENGTH // 5)

        self.password = QLineEdit(self)
        self.password.move(LOGIN_WIDTH // 5, 3 * (LOGIN_LENGTH // 7))

        self.check_pass_button = QPushButton("Проверить", self)
        # self.check_pass_button.resize(WIDTH // 3, LENGTH // 10)
        self.check_pass_button.move(LOGIN_WIDTH // 5, 5 * (LOGIN_LENGTH // 7))

        self.check_pass_button.clicked.connect(self.check_pass_button_click)

    def check_pass_button_click(self):
        name, ok_pressed = QInputDialog.getText(self, "Вход",
                                                "Введите код доступа:")
        if ok_pressed and self.password.text() == "admin":
            self.AdminW = AdminWindow()
            self.AdminW.show()'''


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
        '''dfd
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        self.comboBox.addItems([item[0] for item in cur.execute("SELECT title FROM profs").fetchall()])
        self.pushButton_2.clicked.connect(self.date_filter)

    def date_filter(self):
        cur = self.con.cursor()
        print({self.comboBox.currentIndex() + 1})
        result = cur.execute(f"""
                                     SELECT DISTINCT doctors.name, profs.title, doctors.prof
                                     FROM doctors, profs JOIN doctors_profs
                                     ON doctors.id = doctors_profs.doctors_id AND
                                             profs.id = doctors_profs.profs_id
                                     WHERE profs_id = {self.comboBox.currentIndex() + 1}
                                     """).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))'''

    def initUI(self):
        pass

    """db = QSqlDatabase.addDatabase("QSQLITE")
     # Укажем имя базы данных
     db.setDatabaseName("DataBase.sqlite")
     # И откроем подключение
     db.open()

     # QTableView - виджет для отображения данных из базы
     view = QTableView(self)
     # Создадим объект QSqlTableModel,
     # зададим таблицу, с которой он будет работать,
     #  и выберем все данные
     model = QSqlTableModel(self, db)
     model.setTable("classes")
     model.select()

     # Для отображения данных на виджете
     # свяжем его и нашу модель данных
     view.setModel(model)
     view.move(10, 10)
     view.resize(617, 315)"""

    def clean_all(self):
        self.name_line.setText("")
        self.prof_line.setText("")
        self.education_line.setText("")
        self.experiense_line.setText("")
        self.dates_list.clear()
        self.comboBox.clear()
        self.comboBox.addItem("Выбрать")

    # self.setGeometry(300, 100, 650, 450)
    # self.setWindowTitle('Пример работы с QtSql')
    def change_name_info(self):

            self.clean_all()
            self.con = sqlite3.connect("clinic.sqlite")
            cur = self.con.cursor()
            name = self.names_list.currentItem().text()
            result = cur.execute("SELECT name, prof, education, experience FROM doctors "
                                "WHERE name = '{}'".format(name)).fetchall()
            self.name_line.setText(result[0][0])
            self.prof_line.setText(result[0][1])
            self.education_line.setText(result[0][2])
            self.experiense_line.setText(result[0][3])

            id = cur.execute("SELECT id FROM doctors "
                            "WHERE name = '{}'".format(name)).fetchall()

            request = cur.execute("SELECT title FROM dates "
                                "WHERE doctor_id = {}".format(id[0][0])).fetchall()
            a = self.dates_list.clear()
            if len(request) != 0:
                self.dates_list.addItems([item[0] for item in request])

            self.comboBox.addItems([item[0] for item in cur.execute("SELECT title FROM dates "
                                                                "WHERE taken = 1 and doctor_id = {}".format(
                id[0][0])).fetchall()])
            print(id, [item[0] for item in cur.execute("SELECT title FROM dates "
                                                   "WHERE taken = 1 and doctor_id = {}".format(id[0][0])).fetchall()])


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
            id = cur.execute("SELECT id FROM doctors "
                             "WHERE name = '{}'".format(name)).fetchall()
            for x in self.dl:
                add_text = ("INSERT INTO dates (title, doctor_id) "
                            "VALUES ('{}', '{}')".format(x, id[0][0]))
                count = cur.execute(add_text)
                self.con.commit()
            cur.close()
            self.names_list.addItem(name)
            self.clean_all()
        elif not flag:
            QMessageBox.critical(self, "Ошибка ", "Специалист с таким именем уже существует", QMessageBox.Ok)

    # self.names_list.setCurrentItem(self.name_list.currentItem())

    def edit_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        name = self.name_line.text()
        cur = self.con.cursor()
        print(self.name_line.text(), self.prof_line.text(), self.education_line.text(), self.experiense_line.text())
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
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        name = self.name_line.text()
        if name.replace(" ", "") != "":
            id = cur.execute("SELECT id FROM doctors "
                             "WHERE name = '{}'".format(name)).fetchall()
            result1 = cur.execute("DELETE from doctors WHERE name = '{}'".format(name)).fetchall()
            self.con.commit()
            result2 = cur.execute("DELETE from dates WHERE doctor_id = '{}'".format(id[0][0])).fetchall()
            self.con.commit()
            result3 = cur.execute("DELETE from clients "
                                  "WHERE date_id = (SELECT id FROM dates "
                                  "WHERE doctor_id = {})".format(id[0][0])).fetchall()
            self.con.commit()
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
            print(ex)

    def date_add_button_click(self):
        cur = self.con.cursor()
        id = cur.execute("SELECT id FROM doctors "
                        "WHERE name = '{}'".format(self.names_list.currentItem().text())).fetchall()
        request = ("INSERT INTO dates (title, doctor_id) "
                    "VALUES ('{}', '{}')".format(self.date_choose.text(), id[0][0]))
        result = cur.execute(request).fetchall()
        self.con.commit()
        cur.close()
        self.dates_list.addItem(self.date_choose.text())

    def date_delete_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        cur_item = self.dates_list.currentItem().text()
        if cur_item.replace(" ", "") != "":
            if cur_item in self.dl:
                a = self.dl.index(cur_item)
                self.dl = self.dl[:a] + self.dl[a + 1:]
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
