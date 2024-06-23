import asyncio
from Serial_module import start_serial_reader

async def main():
    transport, _ = await start_serial_reader()
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())



    

