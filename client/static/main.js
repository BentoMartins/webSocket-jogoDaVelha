import { connectWebSocket } from "./ws.js";
import { setStatus } from "./ui.js";

const params = new URLSearchParams(window.location.search);
const roomId = params.get("sala");

if (roomId) {
  connectWebSocket(roomId);
} else {
  setStatus("Criando sala...");
  fetch("/api/create-room")
    .then((res) => res.json())
    .then((data) => {
      const link = document.getElementById("share-link");
      link.href = data.link;
      link.textContent = `Link da sala: ${data.link}`;
      link.classList.remove("hidden");
      link.onclick = (e) => {
        e.preventDefault();
        navigator.clipboard.writeText(data.link);
        setStatus("Link copiado!");
      };
      setStatus("Sala criada! Compartilhe o link e aguarde o outro jogador.");
      connectWebSocket(data.room_id);
    });
}