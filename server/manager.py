import uuid
from game.logic import GameLogic

class RoomManager:
    def __init__(self) -> None:
        self.rooms: dict[str, GameLogic] = {}

    def create_room(self) -> str:
        room_id = str(uuid.uuid4())[:8]
        self.rooms[room_id] = GameLogic()
        return room_id

    def get_room(self, room_id: str) -> GameLogic | None:
        return self.rooms.get(room_id)

    def delete_room(self, room_id: str) -> None:
        if room_id in self.rooms:
            del self.rooms[room_id]