import asyncio
import serial_asyncio
import serial.tools.list_ports
from Data_handler import handle_data
import re
from typing import Optional, List

BAUD_RATE = 115200



class SerialReader(asyncio.Protocol):
    """ A class to handle async serial communication with an ESP32 device.

    :param port: The serial port to connect to. If None, the port will be detected automatically.
    :param baudrate: The baud rate for the serial communication.

    """

    def connection_made(self, transport):
        self.transport = transport
        print('Port opened', transport)

    def data_received(self, data):
        raw_message = data.decode('utf-8').strip()
        accept_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+\.\d+,-?\d+\.\d+,\d+\.\d+"

        if re.match(accept_pattern, raw_message):
            message = raw_message
            print('Data received:', message)
            asyncio.create_task(handle_data(message))


    def connection_lost(self, exc):
        print('Port closed')
        if exc:
            print('Error:', exc)
        asyncio.get_event_loop().stop()


async def detect_port(device_name: str = "Silicon Labs CP210x USB to UART Bridge (COM4)"):
    """ Detecta a porta serial onde o ESP32 está conectado.

    :raises Exception: Se nenhuma porta serial for encontrada.
    """

    waiting_connection = True
    port = None

    print("Aguardando conexão...")


    while waiting_connection:
        ports = list(serial.tools.list_ports.comports())
        found_port = next((port.device for port in ports if device_name in port.description), None)

        if found_port:
            port = found_port
            waiting_connection = False
        else:
            if ports:
                port = ports[0].device
                waiting_connection = False

        await asyncio.sleep(0.5)

    return port



async def start_serial_reader():
    loop = asyncio.get_running_loop()

    found_port = await detect_port()

    transport, protocol = await serial_asyncio.create_serial_connection(loop, SerialReader, found_port, baudrate=BAUD_RATE)
    return transport, protocol
