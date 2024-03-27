from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from SDNController import Ui_LoginPage

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

class LoginPage(QtWidgets.QMainWindow, Ui_LoginPage):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)

    def login(self):
        # Add your login logic here
        # If login is successful:
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())