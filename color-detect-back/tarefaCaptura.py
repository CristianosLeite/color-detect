import os
import cv2 as cv
import numpy as np
import snap7

from flask import Flask
from threading import Thread
from snap7.types import Areas, WordLen
from time import sleep

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class TarefaCaptura(Thread):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.s7 = snap7.client.Client()

        self.cap = cv.VideoCapture(0)
        self.video = None
        self.cam_run = False

        self.lower_color = np.array([0, 0, 0])
        self.upper_color = np.array([0, 0, 0])

        self.plc = {
            'ip': '',
            'rack': '',
            'slot': '',
            'var_cam': ''
        }

        self.db_number = None
        self.start_bit = None

        self.has_plc = False

        self.array_mask = [100, 100, 200, 100, 200, 200, 100, 200]

        self.mask_pos = [(self.array_mask[i], self.array_mask[i+1]) for i in range(0, len(self.array_mask), 2)]

        self.mask = self.config_mask()

    def rgb_to_hsv(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df / mx) * 100
        v = mx * 100
        return int(h), int(s), int(v)

    def config_lower_color(self):
        lower_color = np.array([31, 105, 68], np.uint8)
        return lower_color

    def config_upper_color(self):
        upper_color = np.array([57, 240, 240], np.uint8)
        return upper_color

    def get_colors_limits(self, colors):
        if colors:
            if colors['colormin'] == '' or colors['colormax'] == '':
                self.lower_color = self.config_lower_color()
                self.upper_color = self.config_upper_color()
            else:
                lower_color = colors['colormin'].split(',')
                lower_color_array = [int(int(lower_color[0])/2), int(lower_color[1]), int(lower_color[2])]
                self.lower_color = np.array(lower_color_array)

                upper_color = colors['colormax'].split(',')
                upper_color_array = [int(int(upper_color[0])/2), int(upper_color[1]), int(upper_color[2])]
                self.upper_color = np.array(upper_color_array)

    def gen(self):
        ret, jpeg = cv.imencode('.jpg', self.video)
        return jpeg.tobytes()
    
    def load_mask(self, mask):
        if mask and 'mask' in mask and mask['mask'] is not None:
            self.array_mask = [int(value) for value in mask['mask']]
            self.mask_pos = [(self.array_mask[i], self.array_mask[i+1]) for i in range(0, len(self.array_mask), 2)]
            self.mask = self.config_mask()
            return self.array_mask
        return False

    def config_mask(self):
        img = cv.imread(os.path.join(ROOT_DIR, 'mask.jpg'))
        img_resized = cv.resize(img, (640, 480))
        points = np.array([self.mask_pos], dtype=np.int32)
        poligono_desenhado = cv.fillPoly(img_resized, points, [255, 255, 255], lineType=cv.LINE_AA)
        img_escala_cinza = cv.cvtColor(poligono_desenhado, cv.COLOR_BGR2GRAY)
        ret, mascara = cv.threshold(img_escala_cinza, 254, 255, cv.THRESH_BINARY)
        return mascara

    def modify_mask(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.mask_pos = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.mask = self.config_mask()

    def reset_mask(self):
        self.mask_pos = [(100, 50), (200, 50), (200, 150), (100, 150)]
        self.mask = self.config_mask()
    
    def update_plc(self, plc_banco):
        try:
            if plc_banco:
                plc_api = {key: plc_banco[key] for key in ['ip', 'rack', 'slot', 'var_cam']}
                array_var_cam = plc_api['var_cam'].split(',')
                self.plc = plc_api
                self.db_number, self.start_bit = map(int, array_var_cam[:2])

                sleep(1)
                plc_state = self.s7.get_cpu_state()
                if plc_state != 'S7CpuStatusUnknown':
                    self.has_plc = True
                    return True

                self.connect_to_plc()
                return False
            else:
                print('PLC not registered in the database')
                self.has_plc = False
                return False

        except Exception as e:
            print(f'Error connecting to PLC: {e}')
            if self.reconnect_to_plc():
                return True
            return False

    def connect_to_plc(self):
        try:
            sleep(1)
            self.s7.connect(
                address=self.plc['ip'],
                rack=int(self.plc['rack']),
                slot=int(self.plc['slot']),
                tcpport=102
            )
            print('PLC connected')
        except Exception as e:
            print(f'Error connecting to PLC: {e}')

    def reconnect_to_plc(self):
        try:
            sleep(1)
            self.s7.disconnect()
            sleep(2)
            self.connect_to_plc()
            return True
        except Exception as e:
            print(f'Error reconnecting to PLC: {e}')
            return False

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame = self.cap.read()
            if ret:
                self.cam_run = True
                inspection_mask = cv.bitwise_and(frame, frame, mask=self.mask)
                hsv = cv.cvtColor(inspection_mask, cv.COLOR_BGR2HSV)
                mask_green = cv.inRange(hsv, self.lower_color, self.upper_color)
                kernal = np.ones((5, 5), "uint8")
                mask_green = cv.dilate(mask_green, kernal)

                cv.bitwise_and(inspection_mask, inspection_mask, mask=mask_green)

                contours, hierarchy = cv.findContours(mask_green, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv.contourArea(contour)
                    if area > 50:
                        x, y, w, h = cv.boundingRect(contour)
                        cv.rectangle(inspection_mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv.putText(inspection_mask, "Cor detectada!", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

                        if self.has_plc:
                            try:
                                self.s7.as_write_area(
                                    area=Areas.DB,
                                    dbnumber=self.db_number,
                                    start=self.start_bit,
                                    size=1,
                                    wordlen=WordLen.Bit,
                                    pusrdata=bytearray([0b00000001])
                                )
                            except:                           
                                self.has_plc = False

                self.video = inspection_mask
            else:
                if self.cam_run:
                    print('Ocorreu um erro ao inciar a câmera!')
                    self.cam_run = False
                    self.cap = cv.VideoCapture(0)
                else:
                    print('A câmera foi desligada!')

    def stop(self):
        self.cam_run = False
        self.ThreadActive = False
        self.cap.release()

if __name__ == '__main__':
    app.run()
