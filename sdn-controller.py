from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from ui_main import Ui_MainWindow
from login import Ui_LoginPage
from dhcp_config import Ui_DhcpConfig
from pool_config import Ui_PoolConfig
from bridge_config import Ui_BridgeConfig
from wireless_config import Ui_WirelessConfig
from security_profiles_config import Ui_SecurityProfilesConfig
from dns_config import Ui_DnsConfig
import dhcp_queries
import bridge_queries
import wireless_queries
import security_profile_queries
import dns_queries
import sys
import json
import atexit
import warnings
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, delete
from sqlalchemy.orm import sessionmaker


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, engine, nodes):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.engine = engine 
        self.nodes = nodes

        # Selected
        self.selected_node = []
        self.selected_dhcp = None
        self.selected_bridge = None
        self.selected_wireless = None
        self.selected_sec_profile = None
        self.selected_static_dns = None

        #Auth
        self.ip_address = None
        self.username = None
        self.password = None

        #Pages
        self.dhcp_config_page = None
        self.bridge_config_page = None
        self.wireless_config_page = None
        self.sec_profile_config_page = None
        self.static_dns_page = None


        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.btn_page_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        self.btn_page_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_5))
        self.btn_page_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_6))
        self.btn_page_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_7))
        self.btn_page_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_8))


        # Add Nodes
        self.btn_add.clicked.connect(self.add_node)
        self.btn_config_selected_nodes.clicked.connect(self.configure_selected_nodes)
        self.routerTable.itemClicked.connect(self.handle_table_item_clicked)

        # DHCP
        if self.selected_dhcp is None:
            self.btn_update_dhcp.setEnabled(False)
            self.btn_delete_dhcp.setEnabled(False)
        self.btn_add_dhcp.clicked.connect(self.open_dhcp_config_page) 
        self.btn_update_dhcp.clicked.connect(self.open_dhcp_config_page)
        self.btn_delete_dhcp.clicked.connect(self.open_dhcp_config_page)

        self.dhcptable.itemClicked.connect(self.handle_dhcptable_item_clicked)

        # Interfaces
        self.btn_all.click()
        self.btn_all.clicked.connect(self.refresh_table_interfaces)
        self.btn_physical.clicked.connect(self.refresh_table_interfaces)
        self.btn_wireless.clicked.connect(self.refresh_table_interfaces)
        self.btn_bridge.clicked.connect(self.refresh_table_interfaces)
        self.btn_add_bridge.setEnabled(False)
        self.btn_update_bridge.setEnabled(False)
        self.btn_delete_bridge.setEnabled(False)

        self.btn_add_bridge.clicked.connect(self.open_bridge_config_page)
        self.btn_update_bridge.clicked.connect(self.open_bridge_config_page)
        self.btn_delete_bridge.clicked.connect(self.open_bridge_config_page)

        self.interfacesTable.itemClicked.connect(self.handle_inttable_item_clicked)

        # Wireless
        self.btn_config_wireless.setEnabled(False)

        self.wirelesstable.itemClicked.connect(self.handle_wireTable_item_clicked)
        self.btn_config_wireless.clicked.connect(self.open_wireless_config_page)

        # Security Profiles
        self.btn_update_security_profiles.setEnabled(False)
        self.btn_delete_security_profiles.setEnabled(False)
        self.securityTable.itemClicked.connect(self.handle_secTable_item_clicked)
        
        self.btn_add_security_profiles.clicked.connect(self.open_sec_profile_config_page)
        self.btn_update_security_profiles.clicked.connect(self.open_sec_profile_config_page)
        self.btn_delete_security_profiles.clicked.connect(self.open_sec_profile_config_page)

        # DNS Static
        self.btn_edit_dns.setEnabled(False)
        self.btn_delete_dns.setEnabled(False)

        self.dnstable.itemClicked.connect(self.handle_dnsTable_item_clicked)
        self.btn_add_dns.clicked.connect(self.open_dns_static_config_page)
        self.btn_edit_dns.clicked.connect(self.open_dns_static_config_page)
        self.btn_delete_dns.clicked.connect(self.open_dns_static_config_page)

        # Default
        self.update_button_status()
        self.btn_page_2.setEnabled(False)
        self.btn_page_3.setEnabled(False)
        self.btn_page_4.setEnabled(False)
        self.btn_page_5.setEnabled(False)
        self.btn_page_6.setEnabled(False)
        self.btn_page_7.setEnabled(False)
        self.btn_page_8.setEnabled(False)

        self.refresh_table()

    def open_dhcp_config_page(self):
        sender = self.sender()  
           
        if sender == self.btn_delete_dhcp:           
            dhcp_queries.delete_dhcp_server(self.username,self.password,self.ip_address,self.selected_dhcp['.id'])
            self.refresh_table_dhcp()
        if sender == self.btn_update_dhcp: 
            if self.selected_node is None:
                QtWidgets.QMessageBox.critical(self, "Error", "No node selected.")
                return
            if self.selected_dhcp is not None:
                if not self.dhcp_config_page:
                    self.dhcp_config_page = DhcpPage(self.ip_address, self.username, self.password)
                    self.dhcp_config_page.configSaved.connect(self.handleConfigSaved)
                self.dhcp_config_page.populate_dhcp_data(self.selected_dhcp)
                self.dhcp_config_page.show()
        if sender == self.btn_add_dhcp:
            self.dhcp_config_page = DhcpPage(self.ip_address, self.username, self.password)
            self.dhcp_config_page.configSaved.connect(self.handleConfigSaved)
            self.dhcp_config_page.show()

    def open_bridge_config_page(self):
        sender = self.sender()
        if sender == self.btn_delete_bridge:
            bridge_queries.delete_bridge(self.username,self.password,self.ip_address,self.selected_bridge['.id'])
            self.btn_bridge.click()
            self.refresh_table_interfaces()
        if sender == self.btn_update_bridge:
            self.bridge_config_page = BridgePage(self.ip_address,self.username,self.password)
            self.bridge_config_page.configSaved.connect(self.handleConfigSaved)
            self.bridge_config_page.update_config(self.selected_bridge)
            self.bridge_config_page.show()
        if sender == self.btn_add_bridge:
            self.bridge_config_page = BridgePage(self.ip_address,self.username,self.password)
            self.bridge_config_page.configSaved.connect(self.handleConfigSaved)
            self.bridge_config_page.show()

    def open_wireless_config_page(self):
        self.wireless_config_page = WirelessPage(self.ip_address,self.username,self.password)
        self.wireless_config_page.configSaved.connect(self.handleConfigSaved)
        self.wireless_config_page.fill_wireless_info(self.selected_wireless)
        self.wireless_config_page.show()

    def open_sec_profile_config_page(self):
        sender = self.sender()
        if sender == self.btn_delete_security_profiles:
            security_profile_queries.delete_security_profile(self.username,self.password,self.ip_address,self.selected_sec_profile['.id'])
            self.refresh_table_wireless()
        if sender == self.btn_update_security_profiles:
            self.sec_profile_config_page = SecurityProfilesPage(self.ip_address,self.username,self.password)
            self.sec_profile_config_page.configSaved.connect(self.handleConfigSaved)
            self.sec_profile_config_page.fill_with_security_profile(self.selected_sec_profile)
            self.sec_profile_config_page.show()
        if sender == self.btn_add_security_profiles:
            self.sec_profile_config_page = SecurityProfilesPage(self.ip_address,self.username,self.password)
            self.sec_profile_config_page.configSaved.connect(self.handleConfigSaved)
            
            self.sec_profile_config_page.show()

    def open_dns_static_config_page(self):
        sender = self.sender()
        if sender == self.btn_delete_dns:
            dns_queries.delete_static_dns(self.username,self.password,self.ip_address,self.selected_static_dns['.id'])
            self.refresh_table_dns_static()
        if sender == self.btn_edit_dns:
            self.static_dns_page = DnsStaticPage(self.ip_address,self.username,self.password)
            self.static_dns_page.configSaved.connect(self.handleConfigSaved)
            self.static_dns_page.fill_dns_info(self.selected_static_dns)
            self.static_dns_page.show()
        if sender == self.btn_add_dns:
            self.static_dns_page = DnsStaticPage(self.ip_address,self.username,self.password)
            self.static_dns_page.configSaved.connect(self.handleConfigSaved)
            self.static_dns_page.show()

    def handleConfigSaved(self):
        if self.dhcp_config_page:
            self.dhcp_config_page.hide()
            self.refresh_table_dhcp()
        if self.bridge_config_page:
            self.bridge_config_page.hide()
            self.btn_bridge.click()
            self.refresh_table_interfaces()
        if self.wireless_config_page:
            self.wireless_config_page.hide()
            self.refresh_table_wireless()
        if self.sec_profile_config_page:
            self.sec_profile_config_page.hide()
            self.refresh_table_wireless()
        if self.static_dns_page:
            self.static_dns_page.hide()
            self.refresh_table_dns_static

    def handle_table_item_clicked(self, item):

        row = item.row()
        self.selected_node = self.get_nodes()[row]

        ip_address = self.routerTable.item(row, 1).text()
        Session = sessionmaker(bind=engine)
        session = Session()

        s = self.nodes.select().where(self.nodes.c.ip_address == ip_address)

        data = session.execute(s)
        node = data.fetchone()
        session.commit()
        _, username, password, ip_address, _ = node

        self.ip_address = ip_address
        self.username = username
        self.password = password

        self.refresh_table_dhcp()
        self.refresh_table_interfaces()
        self.refresh_table_wireless()
        self.refresh_table_dns_static()
    
    def handle_dhcptable_item_clicked(self, item):
        self.btn_update_dhcp.setEnabled(True)
        self.btn_delete_dhcp.setEnabled(True)
        row = item.row()
        dhcp_id = self.dhcptable.item(row,0).text()
        self.selected_dhcp = dhcp_queries.get_specific_dhcp_server(self.username,self.password,self.ip_address,dhcp_id)
    
    def handle_inttable_item_clicked(self,item):
        self.btn_update_bridge.setEnabled(True)
        self.btn_delete_bridge.setEnabled(True)
        row = item.row()
        bridge_id = self.interfacesTable.item(row,0).text()
        self.selected_bridge = bridge_queries.get_bridge(self.username,self.password,self.ip_address, bridge_id)

    def handle_wireTable_item_clicked(self,item):
        self.btn_update_security_profiles.setEnabled(False)
        self.btn_delete_security_profiles.setEnabled(False)
        self.btn_config_wireless.setEnabled(True)
        row = item.row()
        wireless_id = self.wirelesstable.item(row,0).text()
        self.selected_wireless = wireless_queries.get_wireless_profile(self.username,self.password,self.ip_address,wireless_id)

    def handle_secTable_item_clicked(self,item):
        self.btn_update_security_profiles.setEnabled(True)
        self.btn_delete_security_profiles.setEnabled(True)
        self.btn_config_wireless.setEnabled(False)
        row = item.row()
        sec_id = self.securityTable.item(row,0).text()
        self.selected_sec_profile = security_profile_queries.get_security_profile(self.username,self.password,self.ip_address, sec_id)

    def handle_dnsTable_item_clicked(self,item):
        self.btn_edit_dns.setEnabled(True)
        self.btn_delete_dns.setEnabled(True)
        row = item.row()
        dns_id = self.dnstable.item(row,0).text()
        self.selected_static_dns = dns_queries.get_static_dns(self.username,self.password,self.ip_address, dns_id)

    def add_node(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        ip_address = self.lineEdit_3.text()
        name = self.lineEdit_4.text()



        response = requests.get(f'https://{ip_address}/rest/ip/address', auth=HTTPBasicAuth(username,password), verify=False)
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
            self.stackedWidget.setCurrentWidget(self.page_2)
            self.update_button_status()
        self.servers = dns_queries.get_dns(self.username,self.password,self.ip_address)
        self.line_servers.setText(self.servers['servers'])
        if self.servers['allow-remote-requests'] == 'true' :
            self.radio_enable.setChecked(True) 
        else:
            self.radio_disable.setChecked(True)
        self.btn_edit_servers.clicked.connect(self.edit_servers)

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
            response= dhcp_queries.get_available_dhcp_servers(self.username,self.password,self.ip_address)
            dhcp_server_data = response
            self.dhcptable.setRowCount(0) 
            for row ,dhcp_server in enumerate(dhcp_server_data):
                
                dhcp_id=dhcp_server.get('.id', '')
                name = dhcp_server.get('name', '')           
                interface = dhcp_server.get('interface', '')  
                lease_time = dhcp_server.get('lease-time', '') 
                address_pool = dhcp_server.get('address-pool', '')
                disabled = dhcp_server.get('disabled', "")

                if disabled == "false":
                    state = "Enabled"
                else:
                    state = "Disabled"
                self.dhcptable.insertRow(row)

                self.dhcptable.setItem(row, 0, QtWidgets.QTableWidgetItem(dhcp_id))
                self.dhcptable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.dhcptable.setItem(row, 2, QtWidgets.QTableWidgetItem(interface))
                self.dhcptable.setItem(row, 3, QtWidgets.QTableWidgetItem(lease_time))
                self.dhcptable.setItem(row, 4, QtWidgets.QTableWidgetItem(address_pool))
                self.dhcptable.setItem(row, 5, QtWidgets.QTableWidgetItem(state))
                self.dhcptable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
                self.dhcptable.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)


        except Exception as e:
            print(f"Error populating DHCP servers: {e}")

    def refresh_table_interfaces(self):
        sender = self.sender()
        endpoint = "interface"
        if sender == self.btn_all:
            endpoint = "interface"
            self.btn_add_bridge.setEnabled(False)
            self.btn_update_bridge.setEnabled(False)
            self.btn_delete_bridge.setEnabled(False)
        elif sender == self.btn_physical:
            endpoint = "interface/ethernet"
            self.btn_add_bridge.setEnabled(False)
            self.btn_update_bridge.setEnabled(False)
            self.btn_delete_bridge.setEnabled(False)
        elif sender == self.btn_wireless:
            endpoint = "interface/wireless"
            self.btn_add_bridge.setEnabled(False)
            self.btn_update_bridge.setEnabled(False)
            self.btn_delete_bridge.setEnabled(False)
        elif sender == self.btn_bridge:
            endpoint = "interface/bridge"
            self.btn_add_bridge.setEnabled(True)
        
        try:   
            response = requests.get(f"https://{self.ip_address}/rest/{endpoint}", auth=HTTPBasicAuth(self.username, self.password), verify=False)
            interface_data = response.json()
            self.interfacesTable.setRowCount(0)

            for row, interface in enumerate(interface_data):
                int_id= interface.get('.id', '')           
                name = interface.get('name', '')
                mac_address = interface.get('mac-address', '')
                intType = interface.get('type', '')

                self.interfacesTable.insertRow(row)
                self.interfacesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(int_id))
                self.interfacesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.interfacesTable.setItem(row, 2, QtWidgets.QTableWidgetItem(mac_address))
                self.interfacesTable.setItem(row, 3, QtWidgets.QTableWidgetItem(intType))


                for col in range(4):
                    self.interfacesTable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            print(f"Error population interfaces: {e}")

    def refresh_table_wireless(self):
        response = wireless_queries.get_wireless_profiles(self.username,self.password,self.ip_address)
        wireless_data = response

        response = security_profile_queries.get_security_profiles(self.username,self.password,self.ip_address)
        security_data = response

        self.wirelesstable.setRowCount(0)
        self.securityTable.setRowCount(0)

        for row, wireless in enumerate(wireless_data):
                int_id= wireless.get('.id', '')           
                name = wireless.get('name', '')
                ssid = wireless.get('ssid', '')
                sec = wireless.get('security-profile', '')

                self.wirelesstable.insertRow(row)
                self.wirelesstable.setItem(row, 0, QtWidgets.QTableWidgetItem(int_id))
                self.wirelesstable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.wirelesstable.setItem(row, 2, QtWidgets.QTableWidgetItem(ssid))
                self.wirelesstable.setItem(row, 3, QtWidgets.QTableWidgetItem(sec))


                for col in range(4):
                    self.wirelesstable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        for row, security in enumerate(security_data):
            int_id = security.get('.id', '')           
            name = security.get('name', '')
            auth = security.get('authentication-types', '')

            self.securityTable.insertRow(row)
            self.securityTable.setItem(row, 0, QtWidgets.QTableWidgetItem(int_id))
            self.securityTable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.securityTable.setItem(row, 2, QtWidgets.QTableWidgetItem(auth))


            for col in range(3):
                self.securityTable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def refresh_table_dns_static(self):
        response = dns_queries.get_static_dnses(self.username,self.password,self.ip_address)

        self.dnstable.setRowCount(0)

        for row, dns_static in enumerate(response):
                int_id= dns_static.get('.id', '')           
                name = dns_static.get('name', '')
                ip_add = dns_static.get('address', '')

                self.dnstable.insertRow(row)
                self.dnstable.setItem(row, 0, QtWidgets.QTableWidgetItem(int_id))
                self.dnstable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.dnstable.setItem(row, 2, QtWidgets.QTableWidgetItem(ip_add))


                for col in range(3):
                    self.dnstable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def get_nodes(self):
        s = self.nodes.select().where(self.nodes.c.id > 0)
        with self.engine.connect() as connection:
            result = connection.execute(s)
            nodes = result.fetchall()
        return nodes

    def edit_servers(self):
        new_server = self.line_servers.text()
        if self.radio_enable.isChecked():
            disabled = "true"
        else:
            disabled = "false"
        params = {
            'servers': new_server,
            'allow-remote-requests': disabled 
        }

        dns_queries.update_dns(self.username,self.password,self.ip_address,params)

    def update_button_status(self):
        page_buttons = [self.btn_page_2, self.btn_page_3, self.btn_page_4,
                        self.btn_page_5, self.btn_page_6, self.btn_page_7, self.btn_page_8]
        enable_buttons = self.selected_node is not None
        for button in page_buttons:
            button.setEnabled(enable_buttons)

class DnsStaticPage(QtWidgets.QMainWindow, Ui_DnsConfig):
    configSaved = pyqtSignal()
    def __init__(self,ip_address,username,password):
        super(DnsStaticPage,self).__init__()
        self.setupUi(self)
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.selected_dns_static = None

        self.btn_add_dns.clicked.connect(self.save_configuration)

    def fill_dns_info(self,selected_dns_static):
        self.line_name.setText(selected_dns_static['name'])
        self.line_address.setText(selected_dns_static['address'])
        self.selected_dns_static = selected_dns_static
        if self.selected_dns_static['disabled'] == 'false' :
            self.radio_enable.setChecked(True) 
        else:
            self.radio_disable.setChecked(True) 

    def save_configuration(self):
        name = self.line_name.text()
        add = self.line_address.text()

        if self.radio_disable.isChecked():
            disabled = "true"
        else:
            disabled = "false"

        params = {
            "name": name,
            "address": add,
            "disabled": disabled
        }

        if self.selected_dns_static is not None :
            dns_queries.update_static_dns(self.username,self.password,self.ip_address,self.selected_dns_static['.id'], params)
        else:
            dns_queries.add_static_dns(self.username,self.password,self.ip_address,params)
        self.configSaved.emit()
        self.close()
        
class SecurityProfilesPage(QtWidgets.QMainWindow, Ui_SecurityProfilesConfig):
    configSaved = pyqtSignal()
    def __init__(self,ip_address,username,password):
        super(SecurityProfilesPage,self).__init__()
        self.setupUi(self)
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.selected_sec_profile = None

        self.checkbox_wpa.hide()
        self.mode_options = ["none", "dynamic-keys"]
        self.combo_mode.addItems(self.mode_options)
        self.toggle_visibility()
        
        self.combo_mode.activated.connect(self.change_mode)
        self.checkbox_wpa.stateChanged.connect(self.toggle_visibility)

        self.btn_apply_policy.clicked.connect(self.save_configuration)

    def fill_with_security_profile(self,selected_sec_profile):
        self.line_name.setText(selected_sec_profile['name'])
        self.line_preShared_key.setText(selected_sec_profile['wpa2-pre-shared-key'])
        self.selected_sec_profile = selected_sec_profile

        mode_index = self.combo_mode.findText(selected_sec_profile['mode'])
        if mode_index != -1:
            self.combo_mode.setCurrentIndex(mode_index)
        if selected_sec_profile['mode'] == "dynamic-keys":
            self.checkbox_wpa.show()
        auth_types = selected_sec_profile['authentication-types']
        if 'wpa2-psk' in auth_types:
            self.checkbox_wpa.setChecked(True)
        else:
            self.checkbox_wpa.setChecked(False)
        
        self.toggle_visibility()

    def change_mode(self):
        selected_mode = self.combo_mode.currentText()

        if selected_mode == "dynamic-keys": 
            self.checkbox_wpa.show()
        else:
            self.checkbox_wpa.hide()
        
        self.toggle_visibility()

    def toggle_visibility(self):
        if self.checkbox_wpa.isChecked():
            self.label_3.show()
            self.line_preShared_key.show()
            self.auth_types = self.checkbox_wpa.text()
        else:
            self.label_3.hide()
            self.line_preShared_key.hide()
            self.auth_types = None

    def save_configuration(self):
        name = self.line_name.text()
        selected_mode = self.combo_mode.currentText()
        if self.auth_types is not None:
            wpa2_pass = self.line_preShared_key.text()
        
        if len(wpa2_pass) < 8 :
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Password must be 8 characters or more")
            msg_box.setStyleSheet("QLabel{ text: white; }")  # Set text color to white
            msg_box.exec_()
            return
        
        params = {
            'name' : name,
            'mode' : selected_mode,
            'authentication-types' : self.auth_types,
            'wpa2-pre-shared-key' : wpa2_pass
        }

        if self.selected_sec_profile is None:
            security_profile_queries.add_security_profile(self.username,self.password,self.ip_address,params)
        else :
            security_profile_queries.edit_security_profile(self.username,self.password,self.ip_address,self.selected_sec_profile['.id'], params)

        self.configSaved.emit()
        self.close()

class WirelessPage(QtWidgets.QMainWindow, Ui_WirelessConfig):
    configSaved = pyqtSignal()
    def __init__(self,ip_address,username,password):
        super(WirelessPage,self).__init__()
        self.setupUi(self)
        self.ip_address= ip_address
        self.username=username
        self.password=password

        self.btn_apply_wireless.clicked.connect(self.save_configuration)
    
    def fill_wireless_info(self, selected_wireless):
        self.line_name.setText(selected_wireless['name'])
        self.line_ssid.setText(selected_wireless['ssid'])
        self.selected_wireless = selected_wireless
        band = self.selected_wireless['band']
        data_sec_profiles = security_profile_queries.get_security_profiles(self.username,self.password,self.ip_address)

        if self.selected_wireless['disabled'] == 'false' :
            self.radio_enable.setChecked(True) 
        else:
            self.radio_disable.setChecked(True) 
    
        self.combo_mode.clear()
        self.combo_channel_width.clear()    

        if band.startswith('2'):
            channel_width_options = ["20/40mhz-eC","20/40mhz-Ce", "20/40mhz-XX"]
        elif band.startswith('5'):
            channel_width_options = ["20/40mhz eC","20/40mhz-Ce", "20/40mhz-XX", "20/40/80mhz-Ceee", "20/40/80mhz-eCee", "20/40/80mhz-eeCe",
                                     "20/40/80mhz-eeeC", "20/40/80mhz-XXXX"]
        self.combo_channel_width.addItems(channel_width_options)

        for profile in data_sec_profiles:
            profile_name = profile.get('name', '')
            self.combo_mode.addItem(profile_name)

        self.combo_mode.setStyleSheet("QComboBox { color: white; }")
        self.combo_channel_width.setStyleSheet("QComboBox { color: white; }")
        index = self.combo_mode.findText(self.selected_wireless['security-profile'])
        if index != -1:
            self.combo_mode.setCurrentIndex(index)
        index2 = self.combo_channel_width.findText(self.selected_wireless['channel-width'])
        if index2 != -1:
            self.combo_channel_width.setCurrentIndex(index2)

    def save_configuration(self):
        name = self.line_name.text()
        ssid = self.line_ssid.text()
        selected_sec_profile = self.combo_mode.currentText()
        selected_channel_width = self.combo_channel_width.currentText()

        if self.radio_disable.isChecked():
            disabled = "true"
        else:
            disabled = "false"

        params = {
            'name': name,
            'ssid': ssid,
            'security-profile': selected_sec_profile,
            'channel-width': selected_channel_width,
            'disabled': disabled
        }

        wireless_queries.edit_wireless_profile(self.username,self.password,self.ip_address,self.selected_wireless['.id'], params)
        self.configSaved.emit()
        self.close()

class BridgePage(QtWidgets.QMainWindow,Ui_BridgeConfig):
    configSaved = pyqtSignal()
    def __init__(self,ip_address,username,password):
        super(BridgePage,self).__init__()
        self.setupUi(self)
        self.ip_address= ip_address
        self.username=username
        self.password=password
        self.selected_bridge = None
        self.ports_to_delete = []


        self.btn_apply_bridge.clicked.connect(self.save_configuration)
        self.interfaceBox = self.findChild(QtWidgets.QGroupBox, "interfaceBox")

        self.update_config(self.selected_bridge)
        
    
    def create_interface_checkboxes(self):
        try:
            response = requests.get(f"https://{self.ip_address}/rest/interface", auth=HTTPBasicAuth(self.username, self.password), verify=False)
            interface_data = response.json()    
            self.selected_interfaces = []

            checkbox_layout = QtWidgets.QVBoxLayout(self.interfaceBox)

            for interface in interface_data:
                interface_name = interface.get('name', '')
                if interface.get('type', '') != "bridge":
                    checkbox = QtWidgets.QCheckBox(interface_name)
                    checkbox.setChecked(False)  
                    checkbox.setStyleSheet("QCheckBox { color: white; }")
                    checkbox_layout.addWidget(checkbox)
                    checkbox.stateChanged.connect(lambda state, name=interface_name: self.handle_checkbox_state_change(state, name))

            if self.selected_bridge is not None:
                response_ports = bridge_queries.get_bridge_ports(self.username, self.password, self.ip_address)
                data_ports = response_ports

                for checkbox in self.interfaceBox.findChildren(QtWidgets.QCheckBox):
                    interface_name = checkbox.text()
                    for intf in data_ports:
                        if intf['bridge'] == self.selected_bridge['name'] and intf['interface'] == interface_name:
                            checkbox.setChecked(True)

        except Exception as e:
            print(f"Error creating interface checkboxes: {e}")
    
    def handle_checkbox_state_change(self, state, name):
        if state == QtCore.Qt.Checked:
            self.selected_interfaces.append(name)
        elif state == QtCore.Qt.Unchecked:
            if name in self.selected_interfaces:
                self.selected_interfaces.remove(name)
    
    def update_config(self, bridge_data):
        self.selected_bridge = bridge_data
        if self.selected_bridge is not None:
            self.line_name.setText(self.selected_bridge['name'])
        self.create_interface_checkboxes()

    def save_configuration(self):
        name = self.line_name.text()

        params = {
            'name': name,
        }
        if self.selected_bridge == None :
            response = bridge_queries.add_bridge(self.username,self.password,self.ip_address, params)
            add_data = response

            for interface in self.selected_interfaces:
                port_params= {
                    'interface': interface,
                    'bridge' : add_data['name']
                }
                bridge_queries.add_bridge_port(self.username,self.password,self.ip_address,port_params)
        else :
            response_ports = bridge_queries.get_bridge_ports(self.username,self.password,self.ip_address)
            data_ports = response_ports

            existing_ports = [port['interface'] for port in data_ports if port['bridge'] == self.selected_bridge['name']]

            for interface in self.selected_interfaces:
                if interface not in existing_ports:
                    port_params = {
                        'interface': interface,
                        'bridge': self.selected_bridge['.id']
                    }
                    bridge_queries.add_bridge_port(self.username, self.password, self.ip_address, port_params)

            for port in data_ports:
                if port['bridge'] == self.selected_bridge['name'] and port['interface'] not in self.selected_interfaces:
                    bridge_queries.delete_bridge_port(self.username, self.password, self.ip_address, port['.id'])

            if name != self.selected_bridge['name']:
                    bridge_queries.edit_bridge(self.username, self.password, self.ip_address, self.selected_bridge['.id'], params)

        self.configSaved.emit()
        self.close() 

class DhcpPage(QtWidgets.QMainWindow, Ui_DhcpConfig):
     
     configSaved = pyqtSignal()
     def __init__(self,ip_address,username,password):
        super(DhcpPage, self).__init__()
        self.setupUi(self)

        self.pool_config_page = None
        self.ip_address= ip_address
        self.username=username
        self.password=password
        self.id = None

        self.btn_update_dhcp.clicked.connect(self.saveConfig)
        self.btn_add_pool.clicked.connect(self.open_pool_config_page)
        self.populate_interfaces()
        self.populate_address_pool()

     def open_pool_config_page(self):
        if not self.pool_config_page:
            self.pool_config_page = PoolPage(self.ip_address, self.username, self.password)
            self.pool_config_page.configSaved.connect(self.handleConfigSaved)
        self.dhcp_config_page.show()

     def parse_lease_time(self,lease_time_str):
        duration = lease_time_str.strip().lower()  
        if duration.endswith('m'):
            minutes = int(duration[:-1])  
            seconds = minutes * 60  # Convert minutes to seconds
        elif duration.endswith('h'):
            hours = int(duration[:-1])  # Extract the numeric part before 'h' as hours
            seconds = hours * 3600  # Convert hours to seconds
        else:
            raise ValueError("Unsupported lease time format")

        return QtCore.QTime(0, 0, 0).addSecs(seconds)
     
     def populate_dhcp_data(self, dhcp_server_data):
        self.line_name.setText(dhcp_server_data['name'])
        lease_time_str = dhcp_server_data['lease-time'] 
        lease_time = self.parse_lease_time(lease_time_str)
        self.lease_time.setTime(lease_time)
        self.id = dhcp_server_data['.id']
        disabled = dhcp_server_data.get('disabled')
        if disabled == "false":
            self.radio_enable.setChecked(True)
        else:
            self.radio_disable.setChecked(True)

     def handleConfigSaved(self):
        if self.pool_config_page:
            self.pool_config_page.hide()
            
     def populate_interfaces(self):
        try:
            response = bridge_queries.get_bridges(self.username,self.password,self.ip_address)
            interface_data = response

            self.interfaces.clear()
            for interface in interface_data:
                interface_name = interface.get('name', '') 
                self.interfaces.addItem(interface_name)
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
        interface = self.interfaces.currentText()
        time = self.lease_time.time().toString("hh:mm:ss")
        if self.radio_disable.isChecked():
            disabled = True
        else:
            disabled = False

        address_pool = self.address_pool.currentText()

        if time == "00:00:00":
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid time: Lease time cannot be zero.")
            return


        params = {
            'address-pool': address_pool,
            'interface': interface,
            'name': name,
            'lease-time': time,
            'disabled': disabled
        }

        if self.id != None:
            dhcp_queries.edit_dhcp_server(self.username,self.password,self.ip_address,self.id,params)
        else :
            dhcp_queries.add_dhcp_server(self.username,self.password,self.ip_address,params)

        self.configSaved.emit()

class PoolPage(QtWidgets.QMainWindow, Ui_PoolConfig):
    configSaved = pyqtSignal()
    def __init__(self,ip_address, username, password):
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
    warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
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
    #clear_db(engine, nodes)
    login_page = LoginPage()
    main_window = MainWindow(engine, nodes)

    login_page.set_stacked_widget(main_window.stackedWidget)

    login_page.show()
    #atexit.register(clear_db,engine,nodes)  # Register clear_db with engine and nodes arguments
    sys.exit(app.exec_())
