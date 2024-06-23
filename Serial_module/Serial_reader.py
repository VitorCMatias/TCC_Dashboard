import asyncio
import serial_asyncio
import serial.tools.list_ports
from Data_handler.Handler import handle_data
import re


SERIAL_DEVICE = 'Silicon Labs CP210x USB to UART Bridge (COM4)'  # Altere conforme necessário
BAUD_RATE = 115200

class SerialReader(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('Port opened', transport)

    def data_received(self, data):
        raw_message = data.decode('utf-8').strip()

        ignore_patterns = [
            r"Connected to COM\d+ at \d+ baud",
            r"ESP-ROM:esp32c6-\d+",
            r"Build:\w+ \d+ \d+",
            r"rst:0x[0-9a-fA-F] \((\w+)\)",
            r"boot:0x[0-9a-fA-F] \((\w+)\)",
            r"SPIWP:0x[0-9a-fA-F]+",
            r"mode:\w+",
            r"clock div:\d+",
            r"load:0x[0-9a-fA-F]+",
            r"len:0x[0-9a-fA-F]+",
            r"entry 0x[0-9a-fA-F]+"
        ]

        if not any(re.match(pattern, raw_message) for pattern in ignore_patterns):
            message = raw_message
            print('Data received:', message)
            asyncio.create_task(handle_data(message))


    def connection_lost(self, exc):
        print('Port closed')
        asyncio.get_event_loop().stop()

async def start_serial_reader():
    loop = asyncio.get_running_loop()

    ports = list(serial.tools.list_ports.comports())
    found_port = next((port.device for port in ports if SERIAL_DEVICE in port.description), None)

    transport, protocol = await serial_asyncio.create_serial_connection(loop, SerialReader, found_port, baudrate=BAUD_RATE)
    return transport, protocol
