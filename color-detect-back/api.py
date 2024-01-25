import socket
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from tarefaCaptura import TarefaCaptura
from credentials import credentials

# Configure PostgreSQL connection parameters


# Initialize PostgreSQL connection
conn = psycopg2.connect(
    host=credentials['DB_HOST'],
    port=credentials['DB_PORT'],
    database=credentials['DB_NAME'],
    user=credentials['DB_USER'],
    password=credentials['DB_PASSWORD']
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Create object for capturing camera 01
tfc01 = TarefaCaptura(0)
tfc01.start()

# ... Your existing code ...

# Camera 01 routes
def genVideoCam01():
    while True:
        try:
            frame = tfc01.gen()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            print('An error occurred')
            return False

@app.route('/cam01')
def video_feed_01():
    return Response(genVideoCam01(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam01/get_status_run', methods=['POST', 'GET'])
def get_status_run_01():
    return {'run': tfc01.cam_run}

@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return {'ip_address': ip_address}
    except Exception as e:
        print('Error fetching IP: ', e)
        return {'error': 'IP not found' }

@app.route('/cam01/plc', methods=['POST', 'GET'])
def conect_plc_01():
    try:
        if request.method == 'POST':
            plcs = request.get_json()
            if plcs:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO plc_cam01 (ip, rack, slot, var_cam)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE
                        SET ip = excluded.ip, rack = excluded.rack, slot = excluded.slot, var_cam = excluded.var_cam;
                    """, (plcs['ip'], plcs['rack'], plcs['slot'], plcs['var_cam']))

                conn.commit()
                conn_plc = tfc01.update_plc()
                return jsonify({"message": "PLC updated successfully!", 'conectado': conn_plc})

        elif request.method == 'GET':
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM plc_cam01;")
                has_plc = cursor.fetchone()

                if has_plc:
                    plc_api = {
                        'ip': has_plc['ip'],
                        'rack': has_plc['rack'],
                        'slot': has_plc['slot'],
                        'var_cam': has_plc['var_cam'],
                    }
                    conn_plc = tfc01.update_plc(has_plc)
                    return jsonify({"plc": plc_api, 'conectado': conn_plc})
                else:
                    return jsonify({"error": "PLC not registered!"})

    except Exception as e:
        return jsonify({"error": f"Failed to save PLC to the database! {str(e)}", 'conectado': False})

# ... Other camera 01 routes ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True, use_reloader=False)
