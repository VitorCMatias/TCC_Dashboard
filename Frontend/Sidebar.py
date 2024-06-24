import streamlit as st

import os
import subprocess





def __get_venv_python():
    if os.name == 'nt':  # Windows
        return os.path.join('.venv', 'Scripts', 'python.exe')
    else:  # Unix ou MacOS
        return os.path.join('.venv', 'bin', 'python')

# Função para iniciar o subprocesso
def __start_backend():
    if st.session_state.process is None:
        venv_python = __get_venv_python()
        st.session_state.process = subprocess.Popen([venv_python, 'Backend/Backend.py'])

# Função para parar o subprocesso
def __stop_backend():
    if st.session_state.process is not None:
        st.session_state.process.terminate()
        st.session_state.process = None

def show(auto_refresh, refresh_frequency):
    # Inicialize a variável de subprocesso
    if 'process' not in st.session_state:
        st.session_state.process = None
        
    with st.sidebar:
        st.write('# Configurações')
        backend_activated = st.toggle("Receber dados")


        if backend_activated:
            __start_backend()
        else:
            __stop_backend()

        auto_refresh = st.toggle("Recarregar automaticamente", disabled= not backend_activated, value=auto_refresh)
        refresh_frequency = st.slider("Tempo de atualização(s)", 1, 10, refresh_frequency, disabled=not(backend_activated and auto_refresh))
