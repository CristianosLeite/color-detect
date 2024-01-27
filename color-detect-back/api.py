import socket
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from tarefaCaptura import TarefaCaptura
from database import db

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
    return Response(generate_frame(tfc01), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam01/get_status_run', methods=['POST', 'GET'])
def get_status_run_01():
    return {'run': tfc01.cam_run}

@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("127.0.0.1", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return {'ip_address': ip_address}
    except Exception as e:
        return {'error': 'IP not found' }

@app.route('/cam01/plc', methods=['POST', 'GET'])
def connect_plc_01():
    try:
        if request.method == 'POST':
            plc = request.get_json()
            if plc:
                db.save_plc(plc)
                print('PLC saved successfully!')
                conn_plc = tfc01.update_plc(plc)
                return jsonify({"message": "PLC updated successfully!", 'conectado': conn_plc})

        elif request.method == 'GET':
            has_plc = db.get_plc()
            if has_plc:
                plc_api = {key: has_plc[key] for key in ['ip', 'rack', 'slot', 'var_cam']}
                conn_plc = tfc01.update_plc(has_plc)
                return jsonify({"plc": plc_api, 'conectado': conn_plc})
            else:
                return jsonify({"error": "PLC not registered!"})

    except Exception as e:
        print('Error saving PLC: ', e)
        return jsonify({"error": f"Failed to save PLC to the database! {str(e)}", 'conectado': False})

@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    if request.method == 'POST':
        colors = request.get_json()
        if colors and 'colormin' in colors and 'colormax' in colors:
            db.save_colors(colors)
            tfc01.get_colors_limits(colors)
            return {"message": "Limite de cores atualizado com sucesso!"}
        else:
            return {"error": "Missing 'colormin' or 'colormax' in request data"}, 400

    elif request.method == 'GET':
        has_color = db.get_colors()
        if has_color:
            tfc01.get_colors_limits(has_color)
            return {"color": has_color}
        else:
            return {"message": "Não há limite de cores cadastrado!"}

@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    if request.method == 'POST':
        masks = request.get_json()
        if masks and 'mask' in masks:
            db.save_mask(masks['mask'])
            mask_model = db.get_mask()
            tfc01.load_mask(mask_model['mask'].split(','))
            tfc01.modify_mask(*mask_model['mask'].split(','))
            return {"message": "Máscara atualizada com sucesso!"}
        else:
            return {"error": "Missing 'mask' in request data"}, 400

    elif request.method == 'GET':
        has_mask = db.get_mask()
        if has_mask and 'mask' in has_mask:
            tfc01.load_mask(has_mask['mask'].split(','))
            tfc01.modify_mask(*has_mask['mask'].split(','))
            return {'mask': has_mask['mask'].split(',')}
        else:
            return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True, use_reloader=False)
