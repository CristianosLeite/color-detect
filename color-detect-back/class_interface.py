import os
import re
import sys
import time
import asyncio
import websockets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from interface.design import Ui_MainWindow


class StatusThread(QThread):
    status_signal = Signal(str)

    def __init__(self, interface):
        QThread.__init__(self)
        self.interface = interface

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.interface.get_status())
        except Exception as e:
            print(f"Error in StatusThread: {e}")
            loop.close()


class Interface(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.showFullScreen()
        self.setWindowFlag(Qt.FramelessWindowHint)

        # threads cameras
        self.thread_cam01 = None

        self.ButtonRestart.clicked.connect(self.execute_reboot)
        self.ButtonShutdown.clicked.connect(self.execute_shutdown)

        # configurar labels para valor inicial
        self.labelIPAddress.setText('API em erro')
        self.labelIPAddress.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LabelStatusCam01.setText('Câmera em erro')
        self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LabelStatusPLC01.setText('PLC desconectado')
        self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")

        self.status_thread = StatusThread(self)
        self.status_thread.status_signal.connect(self.update_camera_status)
        self.status_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_interface)
        self.timer.start(1000)

    def update_interface(self):
        self.status_thread.status_signal.connect(self.update_camera_status)
        self.status_thread.status_signal.connect(self.update_plc_status)
        self.status_thread.status_signal.connect(self.update_api_status)

    def update_camera_status(self, status):
        try:
            if status == 'True':
                self.LabelStatusCam01.setText('Câmera ok')
                self.LabelStatusCam01.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.LabelStatusCam01.setText('Câmera em erro')
                self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")
        except Exception as e:
            print(f"Error in update_camera_status: {e}")

    def update_plc_status(self, status):
        try:
            if status == 'True':
                self.LabelStatusPLC01.setText('PLC conectado')
                self.LabelStatusPLC01.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.LabelStatusPLC01.setText('PLC desconectado')
                self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")
        except Exception as e:
            print(f"Error in update_plc_status: {e}")

    def update_api_status(self, status):
        try:
            ip_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
            if ip_pattern.match(status):
                self.labelIPAddress.setText(str(status))
                self.labelIPAddress.setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.labelIPAddress.setText('API em erro')
                self.labelIPAddress.setStyleSheet("background-color: red; border: 1px solid black;")
        except Exception as e:
            print(f"Error in update_api_status: {e}")

    async def camera_status_client(self):
        while True:
            try:
                async with websockets.connect('ws://localhost:8765') as websocket:
                    while True:
                        status = await websocket.recv()
                        self.update_camera_status(str(status))
            except Exception as e:
                self.LabelStatusCam01.setText('Câmera em erro')
                self.LabelStatusCam01.setStyleSheet("background-color: red; border: 1px solid black;")
                print(f"Error in camera_status_client: {e}")
                await asyncio.sleep(1)

    async def plc_status_client(self):
        while True:
            try:
                async with websockets.connect('ws://localhost:8766') as websocket:
                    while True:
                        status = await websocket.recv()
                        self.update_plc_status(str(status))
            except Exception as e:
                self.LabelStatusPLC01.setText('PLC desconectado')
                self.LabelStatusPLC01.setStyleSheet("background-color: red; border: 1px solid black;")
                print(f"Error in plc_status_client: {e}")
                await asyncio.sleep(1)

    async def api_status_client(self):
        while True:
            try:
                async with websockets.connect('ws://localhost:8767') as websocket:
                    while True:
                        status = await websocket.recv()
                        self.update_api_status(str(status))
            except Exception as e:
                self.labelIPAddress.setText('API em erro')
                self.labelIPAddress.setStyleSheet("background-color: red; border: 1px solid black;")
                print(f"Error in api_status_client: {e}")
                await asyncio.sleep(1)

    async def get_status(self):
        task_cam = asyncio.create_task(self.camera_status_client())
        task_plc = asyncio.create_task(self.plc_status_client())
        task_api = asyncio.create_task(self.api_status_client())
        await asyncio.gather(task_cam, task_plc, task_api)

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
    qt.exec()
    sys.exit(qt.exec())
