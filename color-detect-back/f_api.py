# Implementa a api usando fastapi e uvicorn
import socket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, Request
from tarefaCaptura import TarefaCaptura
from database import db
from sys import exit

app = FastAPI()
tfc01 = TarefaCaptura()
tfc01.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def generate_frame(tfc_instance):
    while True:
        try:
            frame = tfc_instance.gen()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as e:
            print(f"Error generating frame: {e}")
            return False

def get_local_ip_address(remote_host='8.8.8.8'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((remote_host, 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return None

@app.get('/cam01')
async def video_feed_01():
    return StreamingResponse(generate_frame(tfc01), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/cam01/get_status_run')
async def get_status_run_01():
    return {'run': tfc01.cam_run}

@app.get('/cam01/get_plc_status')
async def get_plc_status_01():
    tfc01.update_plc(db.get_plc())
    ip_address = get_local_ip_address(tfc01.plc['ip'])
    if ip_address:
        return {'conectado': tfc01.has_plc, 'ip_address': ip_address}
    else:
        return {'error': 'IP not found'}
    
@app.get('/cam01/get_ip_address')
async def get_ip_address():
    ip_address = get_local_ip_address()
    if ip_address:
        return {'ip_address': ip_address}
    else:
        return {'error': 'IP not found'}
    
@app.post('/cam01/plc')
async def connect_plc_route():
    request = Request
    body = await request.body()
    return update_plc(body)

@app.get('/cam01/plc')
async def get_plc_route():
    return get_plc()

@app.post('/cam01/color')
async def save_color_route():
    request = Request
    body = await request.body()
    return update_color(body)

@app.get('/cam01/color')
async def get_color_route():
    return get_color()

@app.post('/cam01/mask')
async def save_mask_route():
    request = Request
    body = await request.body()
    return update_mask(body)

@app.get('/cam01/mask')
async def get_mask_route():
    return get_mask()

async def update_plc(request: Request):
    plc = await request.json(self=Request)
    if plc:
        db.save_plc(plc)
        tfc01.update_plc(plc)
        return {'message': 'PLC atualizado com sucesso!'}
    else:
        return {'error': 'Nenhum dado foi informado na requisição.'}
    
def get_plc():
    tfc01.update_plc(db.get_plc())
    ip_address = get_local_ip_address(tfc01.plc['ip'])
    if ip_address:
        return {'conectado': tfc01.has_plc, 'ip_address': ip_address}
    else:
        return {'error': 'IP not found'}
    
async def update_color(request: Request):
    color = await request.json(self=Request)
    if color:
        db.save_color(color)
        return {'message': 'Cor atualizada com sucesso!'}
    else:
        return {'error': 'Nenhum dado foi informado na requisição.'}
    
def get_color():
    color = db.get_color()
    if color:
        if color and 'colormin' in color and 'colormax' in color:
            tfc01.update_color(color)
            return {'color': color}
        else:
            return {'error': 'Cor não cadastrada!'}
    
async def update_mask(request: Request):
    mask = request.json()
    if mask and 'mask' in mask:
        db.save_mask(mask['mask'])
        tfc01.update_mask(mask['mask'])
        return {'message': 'Máscara atualizada com sucesso!'}
    else:
        return {'error': 'Nenhum dado foi informado na requisição.'}
    
def get_mask():
    mask = db.get_mask()
    if mask:
        if mask and 'mask' in mask:
            mask['mask'] = mask['mask'].split(',')
            tfc01.update_mask(mask)
            return {'mask': mask}
        else:
            return {'error': 'Máscara não cadastrada!'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4000)
    db.close()
    tfc01.stop()
    exit(0)
