import os
import subprocess

import streamlit as st


def __get_venv_python():
    if os.name == 'nt': 
        return os.path.join('.venv', 'Scripts', 'python.exe')
    else: 
        return os.path.join('.venv', 'bin', 'python')

def __start_backend():
    """
    Essa função inicializa o backend do programa por meio de subprocessos. Por meio dela é possivél iniciar a recepção de dados. Ela foi desenvolvida para simplificar a excução, por meio dela é possivel executar o programa apenas via streamlit.
    """
    if st.session_state.process is None:
        venv_python = __get_venv_python()
        st.session_state.process = subprocess.Popen([venv_python, 'Backend/Backend.py'])

def __stop_backend():
    """
    Essa função finaliza o backend do programa por meio de subprocessos. Por meio dela é possivél finalizar a recepção de dados. Ela foi desenvolvida para simplificar a excução, por meio dela é possivel executar o programa apenas via streamlit.
    """
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
