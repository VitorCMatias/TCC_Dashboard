import subprocess
import os
import sys
import time


# Caminhos para os scripts
backend_script = 'Backend/Backend.py'
frontend_script = 'app.py'

# Caminho para o ambiente virtual
venv_path = '.venv'

# Detecta o sistema operacional para definir o caminho correto para o ativador do ambiente virtual
if os.name == 'nt':  # Windows
    activate_script = os.path.join(venv_path, 'Scripts', 'activate')
else:  # Unix ou MacOS
    activate_script = os.path.join(venv_path, 'bin', 'activate')

# Função para executar um script no contexto do ambiente virtual
def execute_script(command):
    # Comando para ativar o ambiente virtual e executar o script
    if os.name == 'nt':  # Windows
        command = f"{activate_script} && {command}"
        return subprocess.Popen(command, shell=True)
    else:  # Unix ou MacOS
        command = f". {activate_script} && {command}"
        return subprocess.Popen(command, shell=True, executable='/bin/bash')

# Executa os scripts
backend_process = execute_script(f"python {backend_script}")
frontend_process = execute_script(f"streamlit run {frontend_script}")

# Espera pelos processos para manter o script principal em execução

os.remove("mock_data.db")
backend_process.wait()
frontend_process.wait()
