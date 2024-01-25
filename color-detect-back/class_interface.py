import os
import sys
import time
import threading
import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from interface.design import Ui_MainWindow

URL_IP_ADDRESS = 'http://127.0.0.1:4000/cam01/get_ip_address'
URL_STATUS_CAM01 = 'http://127.0.0.1:4000/cam01/get_status_run'
URL_STATUS_PLC_CAM01 = 'http://127.0.0.1:4000/cam01/plc'


class Interface(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.showFullScreen()
        self.setWindowFlag(Qt.FramelessWindowHint)

        # threads cameras
        self.thread_cam01 = None

        # Atualiza endereço IP atual da placa
        self.request_get_ip()

        self.ButtonRestart.clicked.connect(self.execute_reboot)
        self.ButtonShutdown.clicked.connect(self.execute_shutdown)

        # configurar labels para valor inicial
        self.LabelStatusCam01.setText('Câmera em erro')
        self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LabelStatusPLC01.setText('PLC desconectado')
        self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")

        self.get_status_cam01()
        self.get_status_plc01()

    def request_get_ip(self):
        try:
            request = requests.get(URL_IP_ADDRESS)
            req_json = request.json()

            print(req_json)

            if req_json['ip_address']:
                self.labelIPAddress.setText(req_json['ip_address'])
                self.labelIPAddress.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.labelIPAddress.setText('IP não encontrado')
                self.labelIPAddress.setStyleSheet("background-color: red; border: 1px solid black;")
        except Exception as e:
            print('Erro ao buscar ip: ', e)
            self.labelIPAddress.setText('Erro de conexão API')
            self.labelIPAddress.setStyleSheet("background-color: red; border: 1px solid black;")

    def get_status_cam01(self):
        try:
            request = requests.get(URL_STATUS_CAM01)
            req_json = request.json()

            if req_json['run'] == True:
                self.LabelStatusCam01.setText('Câmera ok')
                self.LabelStatusCam01.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.LabelStatusCam01.setText('Câmera em erro')
                self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")
        except:
            self.LabelStatusCam01.setText('Erro de conexão API')
            self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")

    def get_status_plc01(self):
        try:
            request = requests.get(URL_STATUS_PLC_CAM01)
            req_json = request.json()

            if req_json['conectado'] == True:
                self.LabelStatusPLC01.setText('PLC conectado')
                self.LabelStatusPLC01.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.LabelStatusPLC01.setText('PLC desconectado')
                self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")
        except:
            self.LabelStatusPLC01.setText('Erro de conexão API')
            self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")

    def get_status(self):
        while True:
            self.request_get_ip()
            time.sleep(1)
            self.get_status_cam01()
            time.sleep(1)
            self.get_status_plc01()
            time.sleep(1)

    def execute_shutdown(self):
        os.system("sudo shutdown -h now")
        time.sleep(1)

    def execute_reboot(self):
        os.system("sudo shutdown -r now")
        time.sleep(1)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    interface = Interface()
    interface.show()
    threading.Thread(target=interface.get_status).start()
    qt.exec()
