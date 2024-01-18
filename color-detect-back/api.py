import socket

# imports gerais da aplicação
from bson import ObjectId
from flask import Flask, Response
from flask import request
from flask_cors import CORS

# tarefa captura
from tarefaCaptura import TarefaCaptura

# instância MongoDB
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(host="localhost", port=27017)
db = client.colorDetect


#Instância do servidor Flask
app = Flask(__name__)
CORS(app)

#Cria objeto de captura câmera 01
tfc01 = TarefaCaptura(0)
tfc01.start()


############################Câmera 01############################
def genVideoCam01():
    while True:
        try:
            frame = tfc01.gen()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            print('ocorreu o erro 01')
            return False

@app.route('/cam01')
def video_feed_01():
    return Response(genVideoCam01(),
            mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam01/get_status_run', methods=['POST', 'GET'])
def get_status_run_01():
    return {'run': tfc01.cam_run}

@app.route('/cam01/get_ip_address', methods=['POST', 'GET'])
def get_ip_address():
    try:
         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         s.connect(("8.8.8.8",80))
         ip_address = s.getsockname()[0]
         s.close()
         return {'ip_address': ip_address}
    except Exception as e:
        print('Erro ao buscar IP: ', e)
        return {'error': 'IP não encontrado' }

@app.route('/cam01/plc', methods=['POST', 'GET'])
def conect_plc_01():
    try:
        if (request.method == 'POST'):
            plcs = request.get_json()
            if (plcs):
                plc = db.plc_cam01

                hasPlc = plc.find_one()

                if (hasPlc):
                    print(hasPlc)
                    plc.replace_one({'_id': ObjectId(hasPlc['_id'])}, plcs)
                else:
                    plc.insert_one(plcs)

            conn_plc = tfc01.update_plc()
            return {"message": "PLC atualizado com sucesso!", 'conectado': conn_plc}

        if (request.method == 'GET'):
            plc = db.plc_cam01

            hasPlc = plc.find_one()

            if (hasPlc):
                print(hasPlc)
                plc_api = {
                    'ip': hasPlc['ip'],
                    'rack': hasPlc['rack'],
                    'slot': hasPlc['slot'],
                    'var_cam': hasPlc['var_cam'],
                }
                conn_plc = tfc01.update_plc(hasPlc)
                return {"plc": plc_api, 'conectado': conn_plc}
            else:
                return {"error": "PLC não cadastrado!"}
    except:
        return {"error": "Não foi possível salvar PLC no banco de dados!", 'conectado': False}


@app.route('/cam01/color', methods=['POST', 'GET'])
def save_color_01():
    if(request.method == 'POST'):
        colors = request.get_json()
        if(colors):
            colorModel = colors
            color = db.color_cam01

            hasColor = color.find_one()

            if(hasColor):
                print(hasColor)
                color.replace_one({'_id': ObjectId(hasColor['_id'])}, colors)
            else:
                color.insert_one(colorModel)

        tfc01.getColorsLimits()
        return {"message": "Limite de cores atualizado com sucesso!"}

    if(request.method == 'GET'):
        color = db.color_cam01

        hasColor = color.find_one()

        if (hasColor):
            print(hasColor)
            limit_colors = {
                'colorMin': hasColor['colorMin'],
                'colorMax': hasColor['colorMax']
            }

            return {"limit": limit_colors}


@app.route('/cam01/mask', methods=['POST', 'GET'])
def save_mask_01():
    if (request.method == 'POST'):
        masks = request.get_json()
        print(masks)
        if(masks):
            maskModel = masks
            mask = db.mask_cam01

            hasMask = mask.find_one()

            if(hasMask):
                mask.replace_one({'_id': ObjectId(hasMask['_id'])}, masks)
            else:
                mask.insert_one(maskModel)

        tfc01.get_mask()
        return {"message": "Máscara atualizada com sucesso!"}

    if(request.method == 'GET'):
        mask = db.mask_cam01
        hasMask = mask.find_one()

        if(hasMask):
            tfc01.get_mask()
            return {"mask": tfc01.get_mask_api_cam_01()}
        else:
            return {"message": "Não há máscara cadastrada!"}


if __name__ == '__main__':
        app.run(host='0.0.0.0',
                port=4000,
                threaded=True,
                use_reloader=False,
                )