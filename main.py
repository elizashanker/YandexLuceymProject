import sys
from random import randint

from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from sqlite3 import *

WIDTH = 1200
LENGTH = 1500
LOGIN_WIDTH = WIDTH // 3
LOGIN_LENGTH = LENGTH // 5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, WIDTH, LENGTH)
        self.setWindowTitle("Запись в салон красоты")

        # self.text_field = QTextEdit(self)
        # self.text_field.move(0, 100)

        self.specialist_button = QPushButton("Выбрать специалиста", self)
        self.specialist_button.resize(WIDTH // 3, LENGTH // 10)
        self.specialist_button.move(WIDTH // 3, LENGTH // 10)

        self.service_button = QPushButton("Выбрать услугу", self)
        self.service_button.resize(WIDTH // 3, LENGTH // 10)
        self.service_button.move(WIDTH // 3, 3 * (LENGTH // 10))

        self.date_button = QPushButton("Выбрать дату и время", self)
        self.date_button.resize(WIDTH // 3, LENGTH // 10)
        self.date_button.move(WIDTH // 3, 5 * (LENGTH // 10))

        self.login_button = QPushButton("Вход", self)
        self.login_button.resize(WIDTH // 3, LENGTH // 10)
        self.login_button.move(WIDTH // 3, 7 * (LENGTH // 10))

        self.specialist_button.clicked.connect(self.specialist_button_click)
        self.service_button.clicked.connect(self.service_button_click)
        self.date_button.clicked.connect(self.date_button_click)
        self.login_button.clicked.connect(self.login_button_click)

    def specialist_button_click(self):
        self.SpecialistWindow = SpecialistWindow()
        self.SpecialistWindow.show()

    def service_button_click(self):
        self.ServiceWindow = ServiceWindow()
        self.ServiceWindow.show()

    def date_button_click(self):
        self.DateWindow = DateWindow()
        self.DateWindow.show()

    def login_button_click(self):
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()


class SpecialistWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, WIDTH, LENGTH)
        self.setWindowTitle("Выбор специалиста")


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


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
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
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Пример работы с QtSql')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
