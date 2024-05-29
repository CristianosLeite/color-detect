import snap7
from snap7.types import Areas, WordLen
from typing import TypedDict
import database as db


db = db.Database()

class Plc(TypedDict):
    """
    Plc definition

    Example:
    {
        'ip': '
        'rack': '0',
        'slot': '2',
        'var_cam': '1,0'
    }

    var_cam represents the DB and the bit to be read or written
    """
    ip: str
    rack: str
    slot: str
    var_cam: str


class PLC:
    def __init__(self):
        self.s7 = snap7.client.Client()
        self.has_plc = False
        self.data = {
            'ip': '172.18.176.200',
            'rack': '0',
            'slot': '2',
            'var_cam': '1,0'
        }
        self.db_number = self.data['var_cam'].split(',')[0]
        self.start_bit = self.data['var_cam'].split(',')[1]

        self.get_plc()
        self.connect_plc()
        self.get_cpu_state()

    def connect_plc(self):
        try:
            self.s7.connect(
                address=self.data['ip'],
                rack=int(self.data['rack']),
                slot=int(self.data['slot']),
                tcpport=102
            )
            print('PLC conectado com sucesso!')
            self.has_plc = True
            return True
        except Exception as e:
            self.has_plc = False
            print(f"Error in connect_plc: {e}")
            return False

    def update_plc(self, plc: Plc):
        if plc:
            db.save_plc(plc)
            print('PLC atualizado com sucesso!')
            self.data = plc
            return {"statusText": "PLC Atualizado com sucesso!", 'conectado': plc, 'status': 200}
        else:
            return {"statusText": "Nenhum dado foi informado na requisição.", 'status': 400}

    def get_plc_data(self):
        return self.data
        
    def write_area(self):
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
            except Exception as e:
                print(f'Error writing to PLC: {e}')          
                self.has_plc = False

    def close_plc(self):
        self.s7.disconnect()
        self.has_plc = False
        return True
    
    def get_cpu_state(self):
        status = self.s7.get_cpu_state()
        if status == 'S7CpuStatusRun':
            self.has_plc = True
            return True
        else:
            self.has_plc = False
            return False

    def get_plc(self):
        plc = db.get_plc()
        if plc:
            self.data = plc
            self.has_plc = True
            plc = {key: plc[key] for key in ['ip', 'rack', 'slot', 'var_cam']}
            return {"plc": plc, "conectado": True, "status": 200}
        else:
            return {"statusText": "PLC não cadastrado!", "status": 404}
