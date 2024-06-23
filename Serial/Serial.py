import re
import serial
import serial.tools.list_ports
from typing import Optional, List
import time


class SerialReceiver:
    """ A class to handle serial communication with an ESP32 device

    :param port: The serial port to connect to. If None, the port will be detected automatically.
    :param baudrate: The baud rate for the serial communication.

    """

    def __init__(self, port: Optional[str] = None, baudrate: int = 115200) -> None:
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def __detect_port(self, device_name: str = "Silicon Labs CP210x USB to UART Bridge (COM4)") -> None:
        """ Detect the serial port where the ESP32 is connected.

        :raises Exception: If no serial ports are found.
        """

        waiting_connection = True
        while waiting_connection:
            ports = list(serial.tools.list_ports.comports())
            found_port = next((port.device for port in ports if device_name in port.description), None)

            if found_port:
                self.port = found_port
                waiting_connection = False
            else:
                if ports:
                    self.port = ports[0].device
                    waiting_connection = False

            time.sleep(1)

    def connect(self) -> None:
        """Establish the serial connection to the ESP32."""

        while True:
            try:
                if self.port is None:
                    self.__detect_port()

                self.serial_connection = serial.Serial(self.port, self.baudrate)
                break  # Sai do loop se a conexão for bem-sucedida
            except serial.SerialException:
                print("Conexão perdida com o dispositivo. Tentando novamente em 5 segundos...")
                time.sleep(5)  # Espera 5 segundos antes de tentar novamente

    def __get_device_data(self) -> List[str]:
        """ Receive data from the ESP32, separated by commas.

        :raises Exception: If the serial connection is not established.
        :return: A list of data values received from the ESP32.
        """
        if self.serial_connection is None:
            raise ConnectionError("Serial connection not established")

        try:
            data = self.serial_connection.readline().decode('utf-8').strip()
            values = data.split(',')
            return values
        except serial.SerialException:
            # print("Conexão perdida com o dispositivo.")
            self.serial_connection = None  # Reseta a conexão
            self.connect()  # Tenta reconectar
            return []

    def close_connection(self) -> None:
        """Close the serial connection to the ESP32."""
        if self.serial_connection:
            self.serial_connection.close()

    def get_data(self):
        """Obtem os dados da serial e faz um pré-processamento removendo iformações de LOG da ESP-32.

        :return: Dados lidos da ESP32 processados.
        """

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

        data = self.__get_device_data()
        data_str = ' '.join(data)
        if not any(re.match(pattern, data_str) for pattern in ignore_patterns):
            return data
        else:
            return ''


if __name__ == "__main__":
    serial_receiver = SerialReceiver()
    serial_receiver.connect()

    try:
        while True:
            data = serial_receiver.get_data()
            print(data)
    except KeyboardInterrupt:
        serial_receiver.close_connection()

    finally:
        serial_receiver.close_connection()
