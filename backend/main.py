import os
import subprocess
import shutil


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def start_services():
    # Verifica se os comandos estão disponíveis
    if shutil.which("python") is None or shutil.which("npm") is None or shutil.which("ng") is None:
        raise Exception("python, npm or ng command not found. Please make sure they are installed and available in the system PATH.")

    # Inicializa a API Python
    api_process = subprocess.Popen(f"cd {os.path.join(ROOT_DIR, 'api')} && python api.py", shell=True, stdout=subprocess.PIPE)

    # Muda para o diretório do controlador e inicializa a interface
    npm_process = subprocess.Popen(f"cd {os.path.join(ROOT_DIR, 'controller/electron-interface')} && npm run start", shell=True, stdout=subprocess.PIPE)

    # Muda para o diretório do front-end e inicializa a interface
    frontend_process = subprocess.Popen(f"cd {os.path.join(ROOT_DIR, '../frontend')} && ng serve --configuration production", shell=True, stdout=subprocess.PIPE)

    return api_process, npm_process, frontend_process

if __name__ == "__main__":
    api_process, npm_process, frontend_process = start_services()

    # Imprime a saída dos processos
    print(api_process.stdout.read())
    print(npm_process.stdout.read())
    print(frontend_process.stdout.read())
