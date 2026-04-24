import socket
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from server.handlers import CreateRoomHandler, GameWebSocket
from core.logger import setup_logger, get_logger
from core.config import config
from hardware.system import HardwareSystem

setup_logger()
logger = get_logger("ServidorTornado")

def get_local_ip() -> str:
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_connection.connect(("8.8.8.8", 1))
        return socket_connection.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        socket_connection.close()

def make_app() -> Application:
    url_routes = [
        (r"/api/create-room", CreateRoomHandler),
        (r"/ws", GameWebSocket),
        (
            r"/(.*)",
            StaticFileHandler,
            {"path": config.STATIC_PATH, "default_filename": config.DEFAULT_PAGE},
        ),
    ]
    return Application(url_routes, debug=True)

if __name__ == "__main__":
    app = make_app()
    ip = get_local_ip()
    logger.info(f"Servidor rodando em http://{ip}:{config.PORT}")
    hardware = HardwareSystem()
    hardware.startup_sequence(ip)
    app.listen(config.PORT, address=config.LISTEN_ADDRESS)
    IOLoop.current().start()