from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from login import Ui_LoginPage

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
        username = self.username.text()
        password = self.password.text()
        
        # Check if username and password are correct
        if username == "admin" and password == "password":
            print("Login successful!")
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid username or password.")
            print("Invalid username or password.")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())