
from datetime import datetime
from DB import save_to_db



async def handle_data(data):
    # Processa os dados recebidos da ESP32
    try:
        gps_datetime, longitude, latitude, speed = data.split(',')
        
        gps_datetime = datetime.strptime(gps_datetime,'%Y-%m-%d %H:%M:%S')
        longitude = float(longitude)
        latitude = float(latitude)
        speed = float(speed)

        save_to_db(gps_datetime, longitude, latitude, speed)
    except ValueError as e:
        print(f"Error processing data: {e}")

