import socket
import asyncio
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from inspection import Inspection
from sockets import WebsocketServer
from waitress import serve


app = Flask(__name__)

CORS(app)
tfc01 = Inspection()
tfc01.start()
ws = WebsocketServer(tfc01)

def run_api_server():
    print('Server running on port 4000')
    tfc01.api_status = get_local_ip_address()
    serve(app, host='0.0.0.0', port=4000, threads=1, asyncore_use_poll=False, asyncore_loop_timeout=1)

def stop_server():
    tfc01.stop()

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
        tfc01.ip_address = ip_address
        return ip_address
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return "IP inválido"

def get_ip_address():
    ip_address = get_local_ip_address()
    if ip_address:
        tfc01.ip_address = ip_address
        return jsonify({'ip_address': ip_address, 'status': 200})
    else:
        return jsonify({'statusText': 'Endereço IP não encontrado', 'status': 200})
    
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Video Feed
@app.route('/cam01')
def video_feed_01():
    return Response(generate_frame(tfc01), mimetype='multipart/x-mixed-replace; boundary=frame')

# IP Address
@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    ip_address = get_local_ip_address()
    if ip_address:
        return jsonify({'ip_address': ip_address, 'status': 200})
    else:
        return jsonify({'statusText': 'Endereço IP não encontrado', 'status': 200})

# PLC
@app.route('/cam01/plc', methods=['POST', 'GET'])
def connect_plc_01():
    if request.method == 'POST':
        return jsonify(tfc01.update_plc(request.json))
    elif request.method == 'GET':
        return jsonify(tfc01.get_plc())
    else:
        return jsonify({"statusText": "Método não permitido", "status": 405})

# Color
@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    if request.method == 'POST':
        return jsonify(tfc01.update_color(request.json))
    elif request.method == 'GET':
        return jsonify(tfc01.get_color())
    else:
        return jsonify({"statusText": "Método não permitido", "status": 405})

# Mask
@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    if request.method == 'POST':
        return jsonify(tfc01.update_mask(request.json))
    elif request.method == 'GET':
        return jsonify(tfc01.get_mask())
    else:
        return jsonify({"statusText": "Método não permitido", "status": 405})


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(ws.start_server())
    loop.run_in_executor(None, run_api_server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopping server...')
        stop_server()
