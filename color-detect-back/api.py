import socket
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from tarefaCaptura import TarefaCaptura
from credentials import db_credentials
import re

# Configure PostgreSQL connection parameters

# Initialize PostgreSQL connection
conn = psycopg2.connect(
    host=db_credentials['DB_HOST'],
    port=int(db_credentials['DB_PORT']),
    database=db_credentials['DB_NAME'],
    user=db_credentials['DB_USER'],
    password=db_credentials['DB_PASSWORD']
)

# Initialize PostgreSQL extensions
with conn.cursor() as cursor:
    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

# Create table if not exists
with conn.cursor() as cursor:
      # Tabela PLC
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.plc_cam01 (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(15) NULL,
            rack VARCHAR(2) NULL,
            slot VARCHAR(2) NULL,
            var_cam VARCHAR(10) NULL
        )
        TABLESPACE pg_default;
        ALTER TABLE public.plc_cam01
            OWNER to postgres;
    """)

    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM   pg_constraint 
                WHERE  conname = 'plc_cam01_id_unique'
            ) THEN
                ALTER TABLE public.plc_cam01
                ADD CONSTRAINT plc_cam01_id_unique UNIQUE (id);
            END IF;
        END
        $$;
    """)

    # Tabela de cores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.colors_cam01 (
            id SERIAL PRIMARY KEY,
            colormin VARCHAR(50) NULL,
            colormax VARCHAR(50) NULL
        )
        TABLESPACE pg_default;
        ALTER TABLE public.colors_cam01
            OWNER TO postgres;
    """)
    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM   pg_constraint
                WHERE  conname = 'colors_cam01_id_unique'
            ) THEN
                ALTER TABLE public.colors_cam01
                ADD CONSTRAINT colors_cam01_id_unique UNIQUE (id);
            END IF;
        END
        $$;
    """)

    # Tabela de máscara
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.mask_cam01 (
            id SERIAL PRIMARY KEY,
            mask VARCHAR(50) NULL
        )
        TABLESPACE pg_default;
        ALTER TABLE public.mask_cam01
            OWNER TO postgres;
    """)
    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM   pg_constraint
                WHERE  conname = 'mask_cam01_id_unique'
            ) THEN
                ALTER TABLE public.mask_cam01
                ADD CONSTRAINT mask_cam01_id_unique UNIQUE (id);
            END IF;
        END
        $$;
    """)

conn.commit()

# Initialize PostgreSQL cursor
db = conn.cursor(cursor_factory=RealDictCursor)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Create object for capturing camera 01
tfc01 = TarefaCaptura(0)
tfc01.start()

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
            plc = request.get_json()
            if plc:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO public.plc_cam01 (ip, rack, slot, var_cam)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE
                            SET ip = excluded.ip, rack = excluded.rack, slot = excluded.slot, var_cam = excluded.var_cam;
                    """, (re.sub(r'\.0+(\d)', r'.\1', plc['ip']), plc['rack'], plc['slot'], plc['var_cam']))

                    conn.commit()
                    print('PLC saved successfully!')
                    conn_plc = tfc01.update_plc(plc)
                    return jsonify({"message": "PLC updated successfully!", 'conectado': conn_plc})

        elif request.method == 'GET':
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM plc_cam01 ORDER BY id DESC LIMIT 1")
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
        print('Error saving PLC: ', e)
        return jsonify({"error": f"Failed to save PLC to the database! {str(e)}", 'conectado': False})

@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    if(request.method == 'POST'):
        colors = request.get_json()
        if(colors):
            if 'colorMin' in colors and 'colorMax' in colors:
                colorModel = colors
                query = "INSERT INTO public.colors_cam01 (colormin, colormax) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET colormin = excluded.colormin, colormax = excluded.colormax;"
                db.execute(query, (colorModel['colorMin'], colorModel['colorMax']))
                conn.commit()
            else:
                return {"error": "Missing 'colormin' or 'colormax' in request data"}, 400

        tfc01.getColorsLimits()
        return {"message": "Limite de cores atualizado com sucesso!"}

    if(request.method == 'GET'):
        query = "SELECT * FROM public.colors_cam01 ORDER BY id DESC LIMIT 1"
        db.execute(query)
        hasColor = db.fetchone()

        if (hasColor):
            tfc01.getColorsLimits()
            return {"color": hasColor}
        else:
            return {"message": "Não há limite de cores cadastrado!"}

@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    if (request.method == 'POST'):
        masks = request.get_json()
        if(masks):
            if 'mask' in masks:
                maskModel = masks
                query = "INSERT INTO public.mask_cam01 (mask) VALUES (%s) ON CONFLICT (id) DO UPDATE SET mask = excluded.mask;"
                db.execute(query, (maskModel['mask'],))
                conn.commit()
                return {"message": "Máscara atualizada com sucesso!"}
            else:
                return {"error": "Missing 'mask' in request data"}, 400

        tfc01.get_mask()
        return {"message": "Máscara atualizada com sucesso!"}

    if(request.method == 'GET'):
        query = "SELECT * FROM mask_cam01 ORDER BY id DESC LIMIT 1"
        db.execute(query)
        hasMask = db.fetchone()

        if(hasMask):
            tfc01.get_mask()
            return {"mask": tfc01.get_mask_api_cam_01()}
        else:
            return {"message": "Não há máscara cadastrada!"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True, use_reloader=False)
