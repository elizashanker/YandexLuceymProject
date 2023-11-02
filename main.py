import sys
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5 import uic

WIDTH = 1200
LENGTH = 1500
LOGIN_WIDTH = WIDTH // 3
LOGIN_LENGTH = LENGTH // 5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("1.ui", self)
        self.specialist_button.clicked.connect(self.specialist_button_click)
        self.service_button.clicked.connect(self.service_button_click)
        self.date_button.clicked.connect(self.date_button_click)
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
        self.SpW = SpecialistWindow()
        self.SpW.show()

    def service_button_click(self):
        self.ServiceWindow = ServiceWindow()
        self.ServiceWindow.show()

    def date_button_click(self):
        self.DateWindow = DateWindow()
        self.DateWindow.show()

    def login_button_click(self):
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()


class SpecialistWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("3.ui", self)
        self.reception_button.clicked.connect(self.reception_button_click)

    def initUI(self):
        pass
        '''db = QSqlDatabase.addDatabase("QSQLITE")
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
        model.setTable("doctors")
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)'''

    def reception_button_click(self):
        self.make_abs = MakeReceptionBySpecialist()
        self.make_abs.show()


class ServiceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, WIDTH, LENGTH)
        self.setWindowTitle("Выбор услуги")


class DateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, WIDTH, LENGTH)
        self.setWindowTitle("Выбор даты")


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500 + WIDTH // 3, 500 + LENGTH // 2, LOGIN_WIDTH, LOGIN_LENGTH)
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
        if self.password.text() == "admin":
            self.Admin = AdminWindow()
            self.Admin.show()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("AdminWindow.ui", self)
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        self.names_list.addItems([item[0] for item in cur.execute("SELECT name FROM doctors").fetchall()])
        self.new_button.clicked.connect(self.new_button_click)
        self.pick_button.clicked.connect(self.pick_button_click)
        self.edit_button.clicked.connect(self.edit_button_click)
        '''
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

    # self.setGeometry(300, 100, 650, 450)
    # self.setWindowTitle('Пример работы с QtSql')

    def new_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        add_text = ("INSERT INTO doctors (name, prof, education, experience) "
                    "VALUES ('{}', '{}', '{}', '{}')".format(self.name_line.text(), self.prof_line.text(),
                                                             self.education_line.text(), self.experiense_line.text()))
        print(add_text)
        count = cur.execute(add_text)
        self.con.commit()
        cur.close()

    def pick_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        result = cur.execute("SELECT name, prof, education, experience FROM doctors "
                             "WHERE name = '{}'".format("Федя")).fetchall()
        self.name_line.setText(result[0][0])
        self.prof_line.setText(result[0][1])
        self.education_line.setText(result[0][2])
        self.experiense_line.setText(result[0][3])

    def edit_button_click(self):
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        print(self.name_line.text(), self.prof_line.text(), self.education_line.text(), self.experiense_line.text())
        result = cur.execute("UPDATE doctors "
                             "SET name = '{}',prof = '{}', education = '{}', experience = '{}' "
                             "WHERE name = '{}'".format(self.name_line.text(),
                                                       self.prof_line.text(),
                                                       self.education_line.text(),
                                                       self.experiense_line.text(), "Лаврентий")).fetchall()
        self.con.commit()
        cur.close()


class MakeReceptionBySpecialist(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, WIDTH, LENGTH)
        self.setWindowTitle("Запись к врачу")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
