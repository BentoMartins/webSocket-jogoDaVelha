export function setStatus(message) {
    document.getElementById("status-box").textContent = message;
  }
  
  export function showBoard() {
    document.getElementById("board").classList.remove("hidden");
  }
  
  export function showResetButton(onReset) {
    const btn = document.getElementById("reset-btn");
    btn.classList.remove("hidden");
    btn.onclick = onReset;
  }
  
  export function renderBoard(state, mySymbol, onMove) {
    const cells = document.querySelectorAll(".cell");
    cells.forEach((cell) => {
      const row = parseInt(cell.dataset.row);
      const col = parseInt(cell.dataset.col);
      const value = state.board[row][col];
  
      cell.textContent = value ?? "";
      cell.style.color = value === "X" ? "#f87171" : "#60a5fa";
      cell.disabled = state.game_over || value !== null || state.current_turn !== mySymbol;
  
      cell.onclick = () => {
        if (!cell.disabled) onMove(row, col);
      };
    });
  
    document.getElementById("reset-btn").classList.add("hidden");
  }