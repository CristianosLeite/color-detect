import socket
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from tarefaCaptura import TarefaCaptura
from database import db
from sys import exit

app = Flask(__name__)
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

@app.route('/cam01')
def video_feed_01():
    return Response(generate_frame(tfc01), mimetype='multipart/x-mixed-replace; boundary=frame'), 200

@app.route('/cam01/get_status_run', methods=['POST', 'GET'])
def get_status_run_01():
    return {'run': tfc01.cam_run}, 200

@app.route('/cam01/get_plc_status', methods=['POST', 'GET'])
def get_plc_status_01():
    tfc01.update_plc(db.get_plc())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((f"{tfc01.plc['ip']}", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return {'conectado': tfc01.has_plc, 'ip_address': ip_address}, 200

@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("127.0.0.1", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return {'ip_address': ip_address}, 200
    except Exception as e:
        return {'error': 'IP not found' }, 400

@app.route('/cam01/plc', methods=['POST', 'GET'])
def connect_plc_01():
    try:
        if request.method == 'POST':
            plc = request.get_json()
            if plc:
                db.save_plc(plc)
                print('PLC saved successfully!')
                conn_plc = tfc01.update_plc(plc)
                return jsonify({"message": "PLC updated successfully!", 'conectado': conn_plc}), 200
            else:
                return jsonify({"error": "Missing 'plc' in request data"}), 500

        elif request.method == 'GET':
            has_plc = db.get_plc()
            if has_plc:
                plc_api = {key: has_plc[key] for key in ['ip', 'rack', 'slot', 'var_cam']}
                conn_plc = tfc01.update_plc(has_plc)
                return jsonify({"plc": plc_api, 'conectado': conn_plc}), 200
            else:
                return jsonify({"error": "PLC not registered!"}), 200

    except Exception as e:
        print('Error saving PLC: ', e)
        return jsonify({"error": f"Failed to save PLC to the database! {str(e)}"}), 400

@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    try:
        if request.method == 'POST':
            colors = request.get_json()
            if colors and 'colormin' in colors and 'colormax' in colors:
                db.save_colors(colors)
                tfc01.get_colors_limits(colors)
                return {"message": "Limite de cores atualizado com sucesso!"}, 200
            else:
                return {"error": "Missing 'colormin' or 'colormax' in request data"}, 500

        elif request.method == 'GET':
            try:
                has_color = db.get_colors()
                if has_color:
                    tfc01.get_colors_limits(has_color)
                    return {"color": has_color}, 200
                else:
                    return {"message": "Não há limite de cores cadastrado!"}, 200
            except Exception as e:
                print('Error getting colors: ', e)
                return {"error": f"Failed to get colors from the database! {str(e)}"}, 400
    except Exception as e:
        print('Error saving color: ', e)
        return {"error": f"Failed to save color to the database! {str(e)}"}, 400

@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    try:
        if request.method == 'POST':
            masks = request.get_json()
            if masks and 'mask' in masks:
                db.save_mask(masks['mask'])
                mask_model = db.get_mask()
                tfc01.load_mask(mask_model['mask'].split(','))
                tfc01.modify_mask(*mask_model['mask'].split(','))
                return {"message": "Máscara atualizada com sucesso!"}, 200
            else:
                return {"error": "Missing 'mask' in request data"}, 500

        elif request.method == 'GET':
            has_mask = db.get_mask()
            if has_mask and 'mask' in has_mask:
                tfc01.load_mask(has_mask['mask'].split(','))
                tfc01.modify_mask(*has_mask['mask'].split(','))
                return {'mask': has_mask['mask'].split(',')}, 200
            else:
                return {"message": "Não há máscara cadastrada!"}, 200
    except Exception as e:
        print('Error saving mask: ', e)
        return {"error": f"Failed to save mask to the database! {str(e)}"}, 400

if __name__ == '__main__':
    from waitress import serve
    print('Server running on port 4000')
    serve(app, host='0.0.0.0', port=4000, threads=1, asyncore_use_poll=True)
    print('Server stopped')
    tfc01.stop()
    exit(0)
