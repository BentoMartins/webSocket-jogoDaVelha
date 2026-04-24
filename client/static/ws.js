import { renderBoard, setStatus, showBoard, showResetButton } from "./ui.js";

let socket = null;
export let mySymbol = null;

export function connectWebSocket(roomId) {
  const host = window.location.host;
  socket = new WebSocket(`ws://${host}/ws?sala=${roomId}`);

  socket.onopen = () => setStatus("Conectado! Aguardando jogadores...");

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "init") {
      mySymbol = data.symbol;
      setStatus(`Você é o jogador ${data.symbol}`);
    } else if (data.type === "wait") {
      setStatus(data.message);
    } else if (data.type === "update") {
      showBoard();
      renderBoard(data.state, mySymbol, sendMove);
      if (data.state.game_over) {
        const msg = data.state.winner === "Draw"
          ? "Empate!"
          : `Vencedor: ${data.state.winner}!`;
        setStatus(msg);
        showResetButton(() => sendReset());
      } else {
        const meuTurno = data.state.current_turn === mySymbol;
        setStatus(meuTurno ? "Sua vez!" : `Vez do jogador ${data.state.current_turn}`);
      }
    } else if (data.type === "error") {
      setStatus(`Erro: ${data.message}`);
    }
  };

  socket.onclose = () => setStatus("Desconectado do servidor.");
}

export function sendMove(row, col) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: "move", row, col }));
  }
}

export function sendReset() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: "reset" }));
  }
}