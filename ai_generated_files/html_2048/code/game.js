document.addEventListener("DOMContentLoaded", function () {
  const boardElement = document.getElementById("board");
  const newGameButton = document.getElementById("new-game");
  const undoButton = document.getElementById("undo");

  let board = [];
  let score = 0;
  let gameOver = false;
  let previousBoard = [];
  let previousScore = 0;

  initializeBoard();
  generateNewTile();
  generateNewTile();

  function initializeBoard() {
    boardElement.innerHTML = "";

    for (let i = 0; i < 16; i++) {
      const cell = document.createElement("div");
      cell.id = `cell-${i}`;
      cell.classList.add("cell");
      boardElement.appendChild(cell);
      board[i] = 0;
    }

    score = 0;
    gameOver = false;
    previousBoard = [...board];
    previousScore = score;

    undoButton.disabled = true;
    undoButton.removeEventListener("click", undoMove);
  }

  function generateNewTile() {
    const emptyCells = findEmptyCells();

    if (emptyCells.length > 0) {
      const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];

      const randomNumber = Math.random() < 0.9 ? 2 : 4;
      board[randomCell] = randomNumber;

      updateCell(randomCell);

      if (isGameOver()) {
        gameOver = true;
        alert("Game Over");
      }

      previousBoard = [...board];
      previousScore = score;
      undoButton.disabled = false;
      undoButton.addEventListener("click", undoMove);
    }
  }

  function findEmptyCells() {
    return board.reduce((emptyCells, cell, index) => {
      if (cell === 0) {
        emptyCells.push(index);
      }
      return emptyCells;
    }, []);
  }

  function updateCell(cellIndex) {
    const cell = document.getElementById(`cell-${cellIndex}`);

    cell.textContent = board[cellIndex] !== 0 ? board[cellIndex] : "";
    cell.className = `cell tile${board[cellIndex]}`;
  }

  function moveTiles(direction) {
    let moved = false;

    switch (direction) {
      case "up":
        for (let column = 0; column < 4; column++) {
          for (let row = 1; row < 4; row++) {
            let current = row;

            while (current > 0) {
              const above = current - 1;
              const currentIndex = column * 4 + current;
              const aboveIndex = column * 4 + above;

              if (board[aboveIndex] === 0 || board[aboveIndex] === board[currentIndex]) {
                if (board[aboveIndex] === 0) {
                  board[aboveIndex] = board[currentIndex];
                  board[currentIndex] = 0;
                  current--;
                  moved = true;
                } else {
                  if (!document.getElementById(`cell-${aboveIndex}`).classList.contains("combined")) {
                    board[aboveIndex] *= 2;
                    board[currentIndex] = 0;
                    updateScore(board[aboveIndex]);
                    current--;
                    moved = true;
                  }
                }
              } else {
                break;
              }
            }
          }
        }
        break;
      case "down":
        for (let column = 0; column < 4; column++) {
          for (let row = 2; row >= 0; row--) {
            let current = row;

            while (current < 3) {
              const below = current + 1;
              const currentIndex = column * 4 + current;
              const belowIndex = column * 4 + below;

              if (board[belowIndex] === 0 || board[belowIndex] === board[currentIndex]) {
                if (board[belowIndex] === 0) {
                  board[belowIndex] = board[currentIndex];
                  board[currentIndex] = 0;
                  current++;
                  moved = true;
                } else {
                  if (!document.getElementById(`cell-${belowIndex}`).classList.contains("combined")) {
                    board[belowIndex] *= 2;
                    board[currentIndex] = 0;
                    updateScore(board[belowIndex]);
                    current++;
                    moved = true;
                  }
                }
              } else {
                break;
              }
            }
          }
        }
        break;
      case "left":
        for (let row = 0; row < 4; row++) {
          for (let column = 1; column < 4; column++) {
            let current = column;

            while (current > 0) {
              const left = current - 1;
              const currentIndex = row * 4 + current;
              const leftIndex = row * 4 + left;

              if (board[leftIndex] === 0 || board[leftIndex] === board[currentIndex]) {
                if (board[leftIndex] === 0) {
                  board[leftIndex] = board[currentIndex];
                  board[currentIndex] = 0;
                  current--;
                  moved = true;
                } else {
                  if (!document.getElementById(`cell-${leftIndex}`).classList.contains("combined")) {
                    board[leftIndex] *= 2;
                    board[currentIndex] = 0;
                    updateScore(board[leftIndex]);
                    current--;
                    moved = true;
                  }
                }
              } else {
                break;
              }
            }
          }
        }
        break;
      case "right":
        for (let row = 0; row < 4; row++) {
          for (let column = 2; column >= 0; column--) {
            let current = column;

            while (current < 3) {
              const right = current + 1;
              const currentIndex = row * 4 + current;
              const rightIndex = row * 4 + right;

              if (board[rightIndex] === 0 || board[rightIndex] === board[currentIndex]) {
                if (board[rightIndex] === 0) {
                  board[rightIndex] = board[currentIndex];
                  board[currentIndex] = 0;
                  current++;
                  moved = true;
                } else {
                  if (!document.getElementById(`cell-${rightIndex}`).classList.contains("combined")) {
                    board[rightIndex] *= 2;
                    board[currentIndex] = 0;
                    updateScore(board[rightIndex]);
                    current++;
                    moved = true;
                  }
                }
              } else {
                break;
              }
            }
          }
        }
        break;
    }

    if (moved) {
      updateBoard();
      generateNewTile();
    }
  }

  function updateScore(points) {
    score += points;
    document.getElementById("score").textContent = score;
  }

  function isGameOver() {
    const emptyCells = findEmptyCells();

    if (emptyCells.length > 0) {
      return false;
    }

    for (let i = 0; i < 16; i++) {
      const current = board[i];

      if (
        i % 4 !== 3 && current === board[i + 1] ||
        i < 12 && current === board[i + 4]
      ) {
        return false;
      }
    }

    return true;
  }

  function updateBoard() {
    for (let i = 0; i < 16; i++) {
      updateCell(i);
    }
  }

  function handleKeyDown(event) {
    if (gameOver) {
      return;
    }

    switch (event.key) {
      case "ArrowUp":
        moveTiles("up");
        break;
      case "ArrowDown":
        moveTiles("down");
        break;
      case "ArrowLeft":
        moveTiles("left");
        break;
      case "ArrowRight":
        moveTiles("right");
        break;
    }
  }

  function undoMove() {
    if (gameOver) {
      return;
    }

    board = [...previousBoard];
    score = previousScore;

    updateBoard();
    document.getElementById("score").textContent = score;

    undoButton.disabled = true;
    undoButton.removeEventListener("click", undoMove);
  }

  newGameButton.addEventListener("click", function () {
    initializeBoard();
    generateNewTile();
    generateNewTile();
  });

  document.addEventListener("keydown", handleKeyDown);
});