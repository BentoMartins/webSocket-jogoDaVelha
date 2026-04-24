import json
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from core.logger import get_logger
from server.manager import RoomManager

logger = get_logger("Handlers")
room_manager = RoomManager()

class CreateRoomHandler(RequestHandler):
    def get(self) -> None:
        room_id = room_manager.create_room()
        host = self.request.host
        link = f"http://{host}/?sala={room_id}"
        logger.info(f"Nova sala criada: {room_id} | Acesso via: {link}")
        self.write({"room_id": room_id, "link": link})

class GameWebSocket(WebSocketHandler):
    _clients: list["GameWebSocket"] = []

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        GameWebSocket._clients.append(self)
        self.room_id = self.get_argument("sala", None)
        self.player_id = id(self)
        self.symbol: str | None = None

        if not self.room_id:
            self._send_error("ID da Sala não fornecido. Use ?sala=ID")
            return

        self.game = room_manager.get_room(self.room_id)
        if not self.game:
            self._send_error("Sala não encontrada!")
            return

        if self.game.is_full():
            self._send_error("A sala já está cheia.")
            return

        self.symbol = self.game.assign_player(self.player_id)
        self.write_message(json.dumps({"type": "init", "symbol": self.symbol, "room": self.room_id}))

        if self.game.can_start():
            self._broadcast_state()
        else:
            self.write_message(json.dumps({"type": "wait", "message": "Aguardando o segundo jogador entrar pelo link..."}))

    def on_message(self, message: str | bytes) -> None:
        if not self.game or not self.game.can_start():
            self._send_error("O jogo ainda não começou!")
            return

        try:
            data = json.loads(message)
            if not isinstance(data, dict):
                return
            action = data.get("action")
            if action == "move":
                row = data.get("row")
                col = data.get("col")
                if isinstance(row, int) and isinstance(col, int) and self.symbol:
                    if self.game.make_move(row, col, self.symbol):
                        self._broadcast_state()
            elif action == "reset":
                self.game.reset()
                self._broadcast_state()
        except (json.JSONDecodeError, TypeError):
            logger.error("Falha ao processar mensagem JSON inválida")

    def on_close(self) -> None:
        if self in GameWebSocket._clients:
            GameWebSocket._clients.remove(self)
        if hasattr(self, "game") and self.game:
            self.game.remove_player(self.player_id)
            if not self.game.is_full():
                self._broadcast_wait("O oponente desconectou. Aguardando reconexão...")

    def _send_error(self, message: str) -> None:
        self.write_message(json.dumps({"type": "error", "message": message}))
        self.close()

    def _broadcast_state(self) -> None:
        payload = json.dumps({"type": "update", "state": self.game.state.to_dict()})
        self._send_to_room(payload)

    def _broadcast_wait(self, message: str) -> None:
        payload = json.dumps({"type": "wait", "message": message})
        self._send_to_room(payload)

    def _send_to_room(self, message: str) -> None:
        for client in GameWebSocket._clients:
            if hasattr(client, "room_id") and client.room_id == self.room_id:
                client.write_message(message)