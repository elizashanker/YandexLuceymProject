import sys

import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("try.ui", self)  # Загружаем дизайн
        self.con = sqlite3.connect("clinic.sqlite")
        cur = self.con.cursor()
        self.label.setText("ok")
        #self.pushButton.clicked.connect(self.run)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def run(self):
        pass
        #self.label.setText("OK")
        # Имя элемента совпадает с objectName в QTDesigner

    fname = QFileDialog.getOpenFileName(
        self, 'Выбрать картинку', '',
        'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())