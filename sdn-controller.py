from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from login import Ui_LoginPage
import sys
import requests
import atexit
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, delete


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, nodes):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.nodes = nodes


        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))

        self.btn_add.clicked.connect(self.add_node)

    def add_node(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        ip_address = self.lineEdit_3.text()
        name = self.lineEdit_4.text()

        ins = self.nodes.insert().values(username=username, password=password, ip_address=ip_address, name=name)
        engine.execute(ins)

        print("Node added successfully!")

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()

        self.refresh_table()
        pass

    def refresh_table(self):
        # Clear the table
        self.routerTable.setRowCount(0)

        # Add items to the table
        for node in self.get_nodes():
            row = self.routerTable.rowCount()
            self.routerTable.insertRow(row)
            self.routerTable.setItem(row, 0, QtWidgets.QTableWidgetItem(node['name']))
            self.routerTable.setItem(row, 1, QtWidgets.QTableWidgetItem(node['ip_address']))
        pass

    def get_nodes(self):
        global nodes
        s = self.nodes.select().where(self.nodes.c.id > 0)
        result = engine.execute(s)
        nodes = result.fetchall()
        return nodes
    
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
            self.main_window = MainWindow(nodes)
            self.main_window.showMaximized()
            self.stacked_widget.setCurrentIndex(1)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid username or password.")
            print("Invalid username or password.")

def clear_db():
    # Create a delete statement that deletes all rows from the nodes table
    del_stmt = delete(nodes)

    # Execute the delete statement
    engine.execute(del_stmt)

if __name__ == "__main__":

    engine = create_engine('sqlite:///sdn_controller.db', echo=True)

    metadata = MetaData()

    nodes = Table('Nodes', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String),
    Column('password', String),
    Column('ip_address', String),
    Column('name', String)
    )

    metadata.create_all(engine)

    app = QtWidgets.QApplication(sys.argv)
    clear_db()
    login_page = LoginPage()
    main_window = MainWindow(nodes)

    login_page.set_stacked_widget(main_window.stackedWidget)

    login_page.show()
    atexit.register(clear_db)
    sys.exit(app.exec_())
