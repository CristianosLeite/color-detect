import os
import cv2 as cv
import numpy as np
import colorsys
from typing import List
import database as db


db = db.Database()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ArrayMask(List[int]):
    """
    ArrayMask definition

    Example:
    [100, 100, 200, 100, 200, 200, 100, 200]

    Represents the mask position where the first two values are the x and y of the first point, the next two values are the x and y of the second point, and so on.
    """
    x1: int
    y1: int
    x2: int
    y2: int
    x3: int
    y3: int
    x4: int
    y4: int


class Masks():
    """
    Masks definition

    Example:
    {
        'mask': '100,100,200,100,200,200,100,200'
    }
    """
    mask: str

class MaskConfig:
    def __init__(self):
        self.lower_color = np.array([0, 0, 0])
        self.upper_color = np.array([0, 0, 0])
        self.array_mask = [100, 100, 200, 100, 200, 200, 100, 200]
        self.mask_pos = [(self.array_mask[i], self.array_mask[i+1]) for i in range(0, len(self.array_mask), 2)]

        self.get_mask()
        self.get_color()
        self.mask = self.config_mask()
        self.modify_mask(*self.array_mask)

    def config_mask(self):
        img = cv.imread(os.path.join(ROOT_DIR, 'assets/mask.png'), cv.IMREAD_UNCHANGED)
        img_resized = cv.resize(img, (640, 480))
        points = np.array([self.mask_pos], dtype=np.int32)
        fill_polly = cv.fillPoly(img_resized, points, [255, 255, 255], lineType=cv.LINE_AA)
        mask = cv.cvtColor(fill_polly, cv.COLOR_BGR2GRAY)
        _, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
        return mask
    
    def modify_mask(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.mask_pos = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.mask = self.config_mask()
    
    def update_mask(self, masks: Masks):
        if masks and 'mask' in masks:
            db.save_mask(f"{masks['mask'][0]},{masks['mask'][1]},{masks['mask'][2]},{masks['mask'][3]},{masks['mask'][4]},{masks['mask'][5]},{masks['mask'][6]},{masks['mask'][7]}")
            print('Máscara atualizada com sucesso!')
            self.array_mask = [int(value) if value else 0 for value in masks['mask']]
            self.modify_mask(*self.array_mask)
            return {"statusText": "Máscara Atualizada com sucesso!", "status": 200}
        else:
            return {"statusText": "Nenhum dado foi informado na requisição.", "status": 400}

    def get_mask(self):
        has_mask = db.get_mask()
        if has_mask:
            if has_mask and 'mask' in has_mask:
                self.array_mask = [int(value) if value else 0 for value in has_mask['mask'].split(',')]
                has_mask['mask'] = has_mask['mask'].split(',')
                return {"mask": has_mask, 'status': 200}
        else:
            return {"statusText": "Máscara não cadastrada!", 'status': 404}

    def rgb_to_hsv(self, r, g, b):
        r, g, b = float(r) / 255.0, float(g) / 255.0, float(b) / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        h = h * 360
        s = s * 100
        v = v * 100

        return int(h), int(s), int(v)
    
    def order_range(self, lower_color, upper_color):
        n_lower_color = [lower_color[0], lower_color[1], lower_color[2]]
        n_upper_color = [upper_color[0], upper_color[1], upper_color[2]]

        if lower_color[0] > upper_color[0]:
            n_lower_color[0] = upper_color[0]
            n_upper_color[0] = lower_color[0]
        if lower_color[1] > upper_color[1]:
            n_lower_color[1] = upper_color[1]
            n_upper_color[1] = lower_color[1]
        if lower_color[2] > upper_color[2]:
            n_lower_color[2] = upper_color[2]
            n_upper_color[2] = lower_color[2]

        return n_lower_color, n_upper_color

    def process_colors(self, colors):
        hsv_min = self.rgb_to_hsv(int(colors[0][0]), int(colors[0][1]), int(colors[0][2]))
        hsv_min = hsv_min[0] / 2, hsv_min[1] * 1.75, hsv_min[2] * 1.75
        hsv_max = self.rgb_to_hsv(int(colors[1][0]), int(colors[1][1]), int(colors[1][2]))
        hsv_max = hsv_max[0] / 2, hsv_max[1] * 2.55, hsv_max[2] * 2.55
        lower_color, upper_color = self.order_range(hsv_min, hsv_max)
        self.lower_color = np.array(lower_color)
        self.upper_color = np.array(upper_color)

    def update_color(self, colors):
        if colors:
            db.save_colors(colors)
            print('Limite de cor atualizado com sucesso!')
            self.process_colors([colors['colormin'], colors['colormax']])
            return {"statusText": "Limite de cor Atualizado com sucesso!", "status": 200}
        else:
            return {"statusText": "Nenhum dado foi informado na requisição.", "status": 400}

    def get_color(self):
        has_color = db.get_colors()
        if has_color and 'colormin' in has_color:
            colors = [has_color['colormin'].split(','), has_color['colormax'].split(',')]
            self.process_colors(colors)
            return {"color": has_color, "status": 200}
        else:
            return {"statusText": "Limite de cor não cadastrado!", "status": 404}
