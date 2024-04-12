from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from ui_main import Ui_MainWindow
from login import Ui_LoginPage
from dhcp_config import Ui_DhcpConfig
from pool_config import Ui_PoolConfig
import dhcp_queries
import sys
import json
import atexit
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, delete
from sqlalchemy.orm import sessionmaker
from librouteros import connect


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, engine, nodes):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.engine = engine 
        self.nodes = nodes
        self.selected_node = []
        self.ip_address = None
        self.username = None
        self.password = None
        self.dhcp_config_page = None


        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.btn_page_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        self.btn_page_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_5))
        self.btn_page_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_6))
        self.btn_page_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_7))
        self.btn_page_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_8))


        self.btn_add.clicked.connect(self.add_node)
        self.btn_config_selected_nodes.clicked.connect(self.configure_selected_nodes)
        self.btn_add_dhcp.clicked.connect(self.open_dhcp_config_page) 


        self.update_button_status()

        self.routerTable.itemClicked.connect(self.handle_table_item_clicked)

        self.btn_page_2.setEnabled(False)
        self.btn_page_3.setEnabled(False)
        self.btn_page_4.setEnabled(False)
        self.btn_page_5.setEnabled(False)
        self.btn_page_6.setEnabled(False)
        self.btn_page_7.setEnabled(False)
        self.btn_page_8.setEnabled(False)

        self.refresh_table()

    def open_dhcp_config_page(self):
        if not self.dhcp_config_page:
            self.dhcp_config_page = DhcpPage(self.ip_address, self.username, self.password)
            self.dhcp_config_page.configSaved.connect(self.handleConfigSaved)
        self.dhcp_config_page.show()

    def handleConfigSaved(self):
        if self.dhcp_config_page:
            self.dhcp_config_page.hide()
            self.refresh_table_dhcp()

    def handle_table_item_clicked(self, item):
        row = item.row()
        self.selected_node = self.get_nodes()[row]

    def add_node(self):
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        username = self.lineEdit.text()
        self.username = username
        password = self.lineEdit_2.text()
        self.password = password
        ip_address = self.lineEdit_3.text()
        self.ip_address = ip_address
        name = self.lineEdit_4.text()



        response = requests.get(f'https://{ip_address}/rest/ip/address', auth=HTTPBasicAuth(username,password), verify=False)
        print(response)
        if response.status_code == 200:
            # Insert the values into the nodes table
            ins = self.nodes.insert().values(username=username, password=password, ip_address=ip_address, name=name)
            session.execute(ins)

            # Commit the transaction
            session.commit()

            print("Node added successfully!")

            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.routerTable.verticalHeader().setVisible(False)
            self.refresh_table()
            self.refresh_table_dhcp()

            # Close the session
            session.close()
        else:
            return None
        
    def configure_selected_nodes(self):
        selected_nodes_table = self.routerTable.selectedIndexes()
        if self.selected_node:
            self.selected_nodes_text.setText("Selected Nodes:")
            for index in selected_nodes_table:
                current_text= self.selected_nodes_text.text()
                self.selected_nodes_text.setText(f"{current_text}\n {index.data()}")
            print(self.selected_node)
            self.stackedWidget.setCurrentWidget(self.page_2)
            self.update_button_status()

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

    def refresh_table_dhcp(self):
        try:
            response = requests.get(f'https://{self.ip_address}/rest/ip/dhcp-server', auth=HTTPBasicAuth(self.username, self.password), verify=False)
            if response.status_code == 200:
                dhcp_server_data = json.loads(response.text)                
                self.dhcptable.setRowCount(0) 

                for row ,dhcp_server in enumerate(dhcp_server_data):

                    print("OLA OLA DHCP")
                    name = dhcp_server.get('name', '')           
                    interface = dhcp_server.get('interface', '')  
                    lease_time = dhcp_server.get('lease-time', '') 
                    address_pool = dhcp_server.get('address-pool', '')
                    self.dhcptable.insertRow(row)
                    print("OLA OLA DHCP2")

                    self.dhcptable.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
                    self.dhcptable.setItem(row, 1, QtWidgets.QTableWidgetItem(interface))
                    self.dhcptable.setItem(row, 2, QtWidgets.QTableWidgetItem(lease_time))
                    self.dhcptable.setItem(row, 3, QtWidgets.QTableWidgetItem(address_pool))
                self.dhcptable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        except Exception as e:
            print(f"Error populating DHCP servers: {e}")

    def get_nodes(self):
        s = self.nodes.select().where(self.nodes.c.id > 0)
        with self.engine.connect() as connection:
            result = connection.execute(s)
            nodes = result.fetchall()
        return nodes

    def update_button_status(self):
        page_buttons = [self.btn_page_2, self.btn_page_3, self.btn_page_4,
                        self.btn_page_5, self.btn_page_6, self.btn_page_7, self.btn_page_8]
        enable_buttons = self.selected_node is not None
        for button in page_buttons:
            button.setEnabled(enable_buttons)

class DhcpPage(QtWidgets.QMainWindow, Ui_DhcpConfig):
     configSaved = pyqtSignal()
     def __init__(self):
        super(DhcpPage, self).__init__()
        self.setupUi(self)
        self.btn_update_dhcp.clicked.connect(self.saveConfig)

        self.pool_config_page = None

        self.btn_add_pool.clicked.coonect()
        self.populate_interfaces()

     def open_pool_config_page(self):
        if not self.pool_config_page:
            self.pool_config_page = PoolPage(self.ip_address, self.username, self.password)
            self.pool_config_page.configSaved.connect(self.handleConfigSaved)
        self.dhcp_config_page.show()

     def handleConfigSaved(self):
        if self.pool_config_page:
            self.pool_config_page.hide()
            
     def populate_interfaces(self):
        try:
            api = connect(username=self.username, password=self.password, host=self.ip_address)
            response = dhcp_queries.get_available_dhcp_servers(api)
            if response.status_code == 200:
                interface_data = response.json() 

                self.interfaces.clear()

                for interface in interface_data:
                    self.interfaces.addItem(interface['default-name'])  
        except Exception as e:
            print(f"Error populating interfaces: {e}")

     def populate_address_pool(self):
         try:
             response = requests.get(f'https://{self.ip_address}/rest/ip/pool', auth=HTTPBasicAuth(self.username, self.password), verify=False)
             if response.status_code == 200:
                address_pool_data = response.json()

                self.address_pool.clear()
                for addresspool in address_pool_data:
                    self.address_pool.addItem(addresspool['name'])
         except Exception as e:
            print(f"Error populating address_pools: {e}")
             
     def saveConfig(self):
        name = self.line_name.text()
        relay = self.line_relay.text()
        interface = self.interfaces.currentText()
        time = self.lease_time.time()
        address_pool = self.address_pool.currentText()



        self.configSaved.emit()


class PoolPage(QtWidgets.QMainWindow, Ui_PoolConfig):
    configSaved = pyqtSignal()
    def __init__(self):
        super(PoolPage,self).__init__()
        self.setupUi(self)
        self.btn_apply_pool.clicked.connect(self.saveConfig)

    def saveConfig(self):
        name = self.line_name.text()
        address = self.line_addresses.text()

        self.configSaved.emit()


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
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a delete statement that deletes all rows from the nodes table
    del_stmt = delete(nodes)

    # Execute the delete statement
    session.execute(del_stmt)

    # Commit the transaction
    session.commit()
    session.close()

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
