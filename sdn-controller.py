from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from login import Ui_LoginPage
import sys
import atexit
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, delete


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, engine, nodes):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.engine = engine 
        self.nodes = nodes
        self.item_double_clicked = False
        self.selected_node = None

        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.btn_page_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        self.btn_page_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_5))
        self.btn_page_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_6))
        self.btn_page_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_7))
        self.btn_page_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_8))





        self.btn_add.clicked.connect(self.add_node)

        self.routerTable.itemDoubleClicked.connect(self.handle_table_double_click)

        self.btn_page_2.setEnabled(False)
        self.btn_page_3.setEnabled(False)
        self.btn_page_4.setEnabled(False)
        self.btn_page_5.setEnabled(False)
        self.btn_page_6.setEnabled(False)
        self.btn_page_7.setEnabled(False)
        self.btn_page_8.setEnabled(False)

        self.refresh_table()

    def add_node(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        ip_address = self.lineEdit_3.text()
        name = self.lineEdit_4.text()

        ins = self.nodes.insert().values(username=username, password=password, ip_address=ip_address, name=name)
        with self.engine.connect() as connection:
            connection.execute(ins)
            connection.commit()

        print("Node added successfully!")

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()

        self.refresh_table()

    def refresh_table(self):
        try:
            self.routerTable.setRowCount(0)
            
            for row, node in enumerate(self.get_nodes()):
                self.routerTable.insertRow(row)
                self.routerTable.setItem(row, 0, QtWidgets.QTableWidgetItem(node[4])) 
                self.routerTable.setItem(row, 1, QtWidgets.QTableWidgetItem(node[3]))
            self.routerTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.routerTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        except Exception as e:
            print(f"Error in refresh_table: {e}")

    def get_nodes(self):
        s = self.nodes.select().where(self.nodes.c.id > 0)
        with self.engine.connect() as connection:
            result = connection.execute(s)
            nodes = result.fetchall()
        return nodes

    def handle_table_double_click(self, item):
        if item is not None:
            self.item_double_clicked = True
            self.update_button_status()
            row = item.row()
            node = self.get_nodes()[row]
            self.selected_node = self.get_nodes()[row] 

            #self.page_2.label_name.setText(f"Name: {self.selected_node[4]}")
            #self.page_2.label_ip.setText(f"IP Address: {self.selected_node[3]}")
            #self.page_2.label_username.setText(f"Username: {self.selected_node[2]}")

            self.stackedWidget.setCurrentWidget(self.page_2)

    def update_button_status(self):
            # Enable buttons if an item is double-clicked, otherwise disable them
            self.btn_page_2.setEnabled(self.item_double_clicked)
            self.btn_page_3.setEnabled(self.item_double_clicked)
            self.btn_page_4.setEnabled(self.item_double_clicked)
            self.btn_page_5.setEnabled(self.item_double_clicked)
            self.btn_page_6.setEnabled(self.item_double_clicked)
            self.btn_page_7.setEnabled(self.item_double_clicked)
            self.btn_page_8.setEnabled(self.item_double_clicked)

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
        username = self.username.text()
        password = self.password.text()

        # Check if username and password are correct
        if username == "123" and password == "123":
            print("Login successful!")
            # Change to a specific page in the stacked widget
            self.hide()
            self.main_window = MainWindow(engine, nodes)
            self.main_window.showMaximized()
            self.stacked_widget.setCurrentIndex(1)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid username or password.")
            print("Invalid username or password.")

def clear_db(engine, nodes):

    del_stmt = delete(nodes)

    with engine.connect() as connection:
        connection.execute(del_stmt)
        connection.commit()

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
    clear_db(engine, nodes)
    login_page = LoginPage()
    main_window = MainWindow(engine, nodes)

    login_page.set_stacked_widget(main_window.stackedWidget)

    login_page.show()
    atexit.register(clear_db,engine,nodes)  # Register clear_db with engine and nodes arguments
    sys.exit(app.exec_())
