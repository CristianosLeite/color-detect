import os
import signal
import cv2 as cv
import numpy as np
from flask import Flask
from threading import Thread
from plc import PLC
from mask_config import MaskConfig


mc = MaskConfig()
plc = PLC()

app = Flask(__name__)

class Inspection(Thread):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cap = cv.VideoCapture(1)
        self.video = None
        self.cam_run = False
        self.api_status = 'API em erro'

    def gen(self):
        _, jpeg = cv.imencode('.jpg', self.video)
        return jpeg.tobytes()
        
    def get_status_run(self):
        return self.cam_run
    
    def get_plc_status(self):
        return plc.get_cpu_state()
    
    def update_plc(self, plc: PLC):
        return plc.update_plc(plc)
    
    def get_plc(self):
        return plc.get_plc()
    
    def update_color(self, color: dict):
        return mc.update_color(color)
    
    def get_color(self):
        return mc.get_color()
    
    def update_mask(self, mask: dict):
        return mc.update_mask(mask)
    
    def get_mask(self):
        return mc.get_mask()

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            if plc.has_plc is False:
                plc.connect_plc()
        
            ret, frame = self.cap.read()
            if ret:
                self.cam_run = True
                inspection_mask = cv.bitwise_and(frame, frame, mask=mc.mask)
                hsv = cv.cvtColor(inspection_mask, cv.COLOR_BGR2HSV)
                kernal = np.ones((5, 5), "uint8")
                mask = cv.inRange(hsv, mc.lower_color, mc.upper_color)
                mask = cv.dilate(mask, kernal)
                cv.bitwise_and(inspection_mask, inspection_mask, mask=mask)

                contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                for _, contour in enumerate(contours):
                    area = cv.contourArea(contour)
                    if area > 50:
                        x, y, w, h = cv.boundingRect(contour)
                        cv.rectangle(inspection_mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv.putText(inspection_mask, "Cor detectada!", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

                        if plc.has_plc:
                            plc.write_area(plc.data['var_cam'], 1)
                        
                self.video = inspection_mask
            else:
                if self.cam_run:
                    print('Ocorreu um erro ao inciar a câmera!')
                    self.cam_run = False
                    self.cap = cv.VideoCapture(0)

    def stop(self):
        self.cam_run = False
        self.ThreadActive = False
        self.cap.release()
        cv.destroyAllWindows()
        os.kill(os.getpid(), signal.SIGTERM)


if __name__ == '__main__':
    app.run()