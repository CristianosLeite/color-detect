from builtins import print
from threading import Thread
import cv2 as cv
import numpy as np
from flask import Flask
from psycopg2 import extras, connect
from credentials import db_credentials

# Conexão com PLC
import snap7
from snap7.types import Areas, WordLen

# Instância do servidor Flask
app = Flask(__name__)

# Configure PostgreSQL connection parameters
DB_HOST = db_credentials['DB_HOST']
DB_PORT = int(db_credentials['DB_PORT'])
DB_NAME = db_credentials['DB_NAME']
DB_USER = db_credentials['DB_USER']
DB_PASSWORD = db_credentials['DB_PASSWORD']

# Initialize PostgreSQL connection
conn = connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

db = conn.cursor(cursor_factory=extras.RealDictCursor)

class TarefaCaptura(Thread):

    def __init__(self, device_address, parent=None):
        super().__init__(parent)

        # Global
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

        self.hasPlc = False

        # criar variaveis da máscara e seta posições iniciais
        self.array_mask = self.get_mask()

        if (self.array_mask == None):
            self.array_mask = [100, 100, 200, 100, 200, 200, 100, 200]

        self.mask_pos_1_x = self.array_mask[0]
        self.mask_pos_1_y = self.array_mask[1]
        self.mask_pos_2_x = self.array_mask[2]
        self.mask_pos_2_y = self.array_mask[3]
        self.mask_pos_3_x = self.array_mask[4]
        self.mask_pos_3_y = self.array_mask[5]
        self.mask_pos_4_x = self.array_mask[6]
        self.mask_pos_4_y = self.array_mask[7]

        # configuração inicial da máscara
        self.mask = self.configura_mascara(self.mask_pos_1_x,
                                           self.mask_pos_1_y,
                                           self.mask_pos_2_x,
                                           self.mask_pos_2_y,
                                           self.mask_pos_3_x,
                                           self.mask_pos_3_y,
                                           self.mask_pos_4_x,
                                           self.mask_pos_4_y)

        self.getColorsLimits(device_address)

        query = "SELECT * FROM plc_cam01"
        params = ('plc_cam01')
        db.execute(query, params)
        plc_banco = db.fetchone()

        self.update_plc(plc_banco)

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
    
    def getColorsLimitsApiCam01(self):
        query = "SELECT * FROM colors_cam01 ORDER BY id DESC LIMIT 1"
        db.execute(query)
        hasColor = db.fetchone()

        if (hasColor):
            return hasColor
        else:
            return False

    def getColorsLimits(self, device_address=None):
        query = "SELECT * FROM colors_cam01 ORDER BY id DESC LIMIT 1"
        params = ('colors_cam01')
        db.execute(query, params)
        hasColor = db.fetchone()

        print('hasColor: ', hasColor)

        if(hasColor):
            print(hasColor)
            lower_color = hasColor['colormin'].split(',')
            lower_color_array = [int(int(lower_color[0])/2), int(lower_color[1]), int(lower_color[2])]
            self.lower_color = np.array(lower_color_array)

            upper_color = hasColor['colormax'].split(',')
            upper_color_array = [int(int(upper_color[0])/2), int(upper_color[1]), int(upper_color[2])]
            self.upper_color = np.array(upper_color_array)

    def get_mask(self):
        query = "SELECT * FROM mask_cam01"
        params = ('mask_cam01')
        db.execute(query, params)
        hasMask = db.fetchone()

        if(hasMask):
            if 'mask' in hasMask and hasMask['mask'] is None:
                return False
            
            array_mask = hasMask['mask'].split(',')
            self.array_mask = [int(array_mask[0]),int(array_mask[1]),int(array_mask[2]),
                               int(array_mask[3]),int(array_mask[4]),int(array_mask[5]),
                               int(array_mask[6]),int(array_mask[7])]


            self.mask = self.configura_mascara(self.array_mask[0],
                                               self.array_mask[1],
                                               self.array_mask[2],
                                               self.array_mask[3],
                                               self.array_mask[4],
                                               self.array_mask[5],
                                               self.array_mask[6],
                                               self.array_mask[7])
            return self.array_mask

    def get_mask_api_cam_01(self):
        query = "SELECT * FROM mask_cam01 ORDER BY id DESC LIMIT 1"
        params = ('mask')
        db.execute(query, params)
        hasMask = db.fetchone()

        if(hasMask and 'mask' in hasMask):
            return hasMask['mask'].split(',')
        else:
            return False

    def update_plc(self, plc_banco):
        try:
            if plc_banco:
                plc_api = {
                    'ip': plc_banco['ip'],
                    'rack': plc_banco['rack'],
                    'slot': plc_banco['slot'],
                    'var_cam': plc_banco['var_cam'],
                }
                array_var_cam = plc_api['var_cam'].split(',')
                self.plc = plc_api
                self.db_number = int(array_var_cam[0])
                self.start_bit = int(array_var_cam[1])

                plc_state = self.s7.get_cpu_state()
                print('PLC state: ', plc_state)
                if plc_state != 'S7CpuStatusUnknown':
                    self.hasPlc = True
                    return True

                self.s7.connect(
                    address=self.plc['ip'],
                    rack=int(self.plc['rack']),
                    slot=int(self.plc['slot']),
                    tcpport=102
                )
                print('PLC connected')
                return True
            else:
                print('PLC não cadastrado no banco de dados')
                self.hasPlc = False
                return False

        except Exception as e:
            print('Erro ao conectar ao PLC: ', e)
            try:
                self.s7.disconnect()
                self.s7.connect(
                    address=self.plc['ip'],
                    rack=int(self.plc['rack']),
                    slot=int(self.plc['slot']),
                    tcpport=102
                )

                return True
            except Exception as e:
                print('Erro ao conectar ao PLC 2ª tentativa: ', e)

            return False

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame = self.cap.read()
            if ret:
                self.cam_run = True
                # faz um AND da imgem gerando assim a máscara de inspeção
                inspection_mask = cv.bitwise_and(frame, frame, mask=self.mask)

                # efeito blur
                #blur = cv.GaussianBlur(roi_mascara, (self.desfoque_x, self.desfoque_y), 0)

                hsv = cv.cvtColor(inspection_mask, cv.COLOR_BGR2HSV)

                mask_green = cv.inRange(hsv, self.lower_color, self.upper_color)

                kernal = np.ones((5, 5), "uint8")

                mask_green = cv.dilate(mask_green, kernal)

                # faz um AND da imgem gerando assim a máscara verde
                cv.bitwise_and(inspection_mask, inspection_mask, mask=mask_green)

                contours, hierarchy = cv.findContours(mask_green, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv.contourArea(contour)
                    if (area > 50):
                        x, y, w, h = cv.boundingRect(contour)
                        cv.rectangle(inspection_mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv.putText(inspection_mask, "Cor detectada!", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

                        if(self.hasPlc):
                            try:
                                self.s7.as_write_area(
                                    area=Areas.DB,
                                    dbnumber=self.db_number,
                                    start=self.start_bit,
                                    size=1,
                                    wordlen=WordLen.Bit,
                                    pusrdata=bytearray([0b00000001])
                                )
                                #print('escreveu no PLC')
                            except:                           
                                self.hasPlc = False
                                #print('Erro ao escrever no PLC')
                            
                self.video = inspection_mask
            else:
                print('Ocorreu um erro ao inciar a câmera!')
                self.cam_run = False
                self.cap = cv.VideoCapture(0)


    def gen(self):
        ret, jpeg = cv.imencode('.jpg', self.video)
        return jpeg.tobytes()

    def configura_mascara(self, x1, y1, x2, y2, x3, y3, x4, y4):
        img = cv.imread('C:/Users/crist/OneDrive/Documentos/GitHub/color-detect/color-detect-back/mask.jpg')
        img_resized = cv.resize(img, (640, 480))
        points = np.array([[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]])
        print(points)
        poligono_desenhado = cv.fillPoly(img_resized, points, [255, 255, 255], lineType=cv.LINE_AA)
        img_escala_cinza = cv.cvtColor(poligono_desenhado, cv.COLOR_BGR2GRAY)
        ret, mascara = cv.threshold(img_escala_cinza, 254, 255, cv.THRESH_BINARY)
        return mascara

    def modifica_mascara(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.mask_pos_1_x = x1
        self.mask_pos_1_y = y1
        self.mask_pos_2_x = x2
        self.mask_pos_2_y = y2
        self.mask_pos_3_x = x3
        self.mask_pos_3_y = y3
        self.mask_pos_4_x = x4
        self.mask_pos_4_y = y4
        self.mask = self.configura_mascara(x1, y1, x2, y2, x3, y3, x4, y4)

    def resetar_mascara(self):
        self.mask_pos_1_x = 100
        self.mask_pos_1_y = 50
        self.mask_pos_2_x = 200
        self.mask_pos_2_y = 50
        self.mask_pos_3_x = 200
        self.mask_pos_3_y = 150
        self.mask_pos_4_x = 100
        self.mask_pos_4_y = 150
        self.mask = self.configura_mascara(self.mask_pos_1_x,
                                           self.mask_pos_1_y,
                                           self.mask_pos_2_x,
                                           self.mask_pos_2_y,
                                           self.mask_pos_3_x,
                                           self.mask_pos_3_y,
                                           self.mask_pos_4_x,
                                           self.mask_pos_4_y)

    def configura_cor_low(self):
        lower_color = np.array([31, 105, 68], np.uint8)
        return lower_color

    def configura_cor_high(self):
        upper_color = np.array([57, 240, 240], np.uint8)
        return upper_color
