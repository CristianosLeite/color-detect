import socket
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from tarefaCaptura import TarefaCaptura
from database import db
from sys import exit
from waitress import serve

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

CORS(app)

tfc01 = TarefaCaptura()
tfc01.start()

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
    
@app.route('/cam01')
def video_feed_01():
    return Response(generate_frame(tfc01), mimetype='multipart/x-mixed-replace; boundary=frame'), 200

@app.route('/cam01/get_status_run', methods=['POST', 'GET'])
def get_status_run_01():
    return jsonify({'run': tfc01.cam_run}), 200

@app.route('/cam01/get_plc_status', methods=['POST', 'GET'])
def get_plc_status_01():
    tfc01.update_plc(db.get_plc())
    ip_address = get_local_ip_address(tfc01.plc['ip'])
    if ip_address:
        return jsonify({'conectado': tfc01.has_plc, 'ip_address': ip_address}), 200
    else:
        return jsonify({'statusText': 'IP not found'}), 400

@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    ip_address = get_local_ip_address()
    if ip_address:
        return jsonify({'ip_address': ip_address}), 200
    else:
        return jsonify({'statusText': 'IP not found'}), 400

@app.route('/cam01/plc', methods=['POST', 'GET'])
def connect_plc_01():
    if request.method == 'POST':
        return update_plc()
    elif request.method == 'GET':
        return get_plc()

def update_plc():
    plc = request.get_json()
    if plc:
        db.save_plc(plc)
        print('PLC atualizado com sucesso!')
        conn_plc = tfc01.update_plc(plc)
        return jsonify({"statusText": "PLC Atualizado com sucesso!", 'conectado': conn_plc}), 200
    else:
        return jsonify({"statusText": "Nenhum dado foi informado na requisição."}), 400

def get_plc():
    has_plc = db.get_plc()
    if has_plc:
        plc_api = {key: has_plc[key] for key in ['ip', 'rack', 'slot', 'var_cam']}
        conn_plc = tfc01.update_plc(has_plc)
        return jsonify({"plc": plc_api, 'conectado': conn_plc}), 200
    else:
        return jsonify({"statusText": "PLC não cadastrado!"}), 404

@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    if request.method == 'POST':
        return update_color()
    elif request.method == 'GET':
        return get_color()
    else:
        return jsonify({"statusText": "Método não permitido"}), 405

def update_color():
    colors = request.get_json()
    if colors:
        db.save_colors(colors)
        print('Limite de cor atualizado com sucesso!')
        tfc01.update_color(colors)
        return jsonify({"statusText": "Limite de cor Atualizado com sucesso!", "status": 200})
    else:
        return jsonify({"statusText": "Nenhum dado foi informado na requisição.", "status": 400})

def get_color():
    has_color = db.get_colors()
    if has_color and 'colormin' in has_color:
        tfc01.update_color(has_color)
        return jsonify({"color": has_color}), 200
    else:
        return jsonify({"statusText": "Limite de cor não cadastrado!"}), 404

@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    if request.method == 'POST':
        return update_mask()
    elif request.method == 'GET':
        return get_mask()

def update_mask():
    masks = request.get_json()
    if masks and 'mask' in masks:
        db.save_mask(f"{masks['mask'][0]},{masks['mask'][1]},{masks['mask'][2]},{masks['mask'][3]},{masks['mask'][4]},{masks['mask'][5]},{masks['mask'][6]},{masks['mask'][7]}")
        print('Máscara atualizada com sucesso!')
        tfc01.update_mask([masks['mask']])
        return jsonify({"statusText": "Máscara Atualizada com sucesso!", "status": 200})
    else:
        return jsonify({"statusText": "Nenhum dado foi informado na requisição.", "status": 400})

def get_mask():
    has_mask = db.get_mask()
    if has_mask:
        if has_mask and 'mask' in has_mask:
            has_mask['mask'] = has_mask['mask'].split(',')
            tfc01.update_mask(has_mask)
            return jsonify({"mask": has_mask}), 200
    else:
        return jsonify({"statusText": "Máscara não cadastrada!"}), 404

if __name__ == '__main__':
    print('Server running on port 4000')
    serve(app, host='0.0.0.0', port=4000, threads=1, asyncore_use_poll=False, asyncore_loop_timeout=1)
    db.close()
    print('Server stopped')
    tfc01.stop()
    exit(0)
