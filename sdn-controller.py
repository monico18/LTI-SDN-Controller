from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from login import Ui_LoginPage
import sys
import requests
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))


        self.btn_add.clicked.connect()

class LoginPage(QtWidgets.QMainWindow, Ui_LoginPage):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.setupUi(self)
        self.username.setFocus()
        self.pushButton.clicked.connect(self.login)

        # Access stacked widget from the MainWindow instance
        self.stacked_widget = None

    def set_stacked_widget(self, stacked_widget):
        self.stacked_widget = stacked_widget

    def login(self):
        # Add your login logic here
        # If login is successful:
        username = self.username.text()
        password = self.password.text()
        
        # Check if username and password are correct
        if username == "admin" and password == "password":
            print("Login successful!")
            # Change to a specific page in the stacked widget
            self.hide()
            self.main_window = MainWindow()
            self.main_window.showMaximized()
            self.stacked_widget.setCurrentIndex(1)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid username or password.")
            print("Invalid username or password.")


if __name__ == "__main__":

    engine = create_engine('sqlite:///sdn_controller.db', echo=True)

    metadata = MetaData()

    users = Table('Routers', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
    Column('ip_address', String),
    Column('name', String)
    )

    metadata.create_all(engine)

    app = QtWidgets.QApplication(sys.argv)
    
    login_page = LoginPage()
    main_window = MainWindow()

    login_page.set_stacked_widget(main_window.stackedWidget)

    login_page.show()

    sys.exit(app.exec_())
