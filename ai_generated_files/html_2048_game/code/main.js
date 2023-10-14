(function() {
  const newGameButton = document.getElementById("new-game-button");
  const gameBoard = document.getElementById("game-board");

  if(!newGameButton || !gameBoard) throw new Error("Unable to get game elements");

  newGameButton.addEventListener("click", startNewGame);
  document.addEventListener('keydown', moveTiles);

  function startNewGame() {
    newGameButton.disabled = true;
    const matrix = getInitialGameMatrix();
    setupGameBoard(matrix);
    newGameButton.disabled = false;
  }

  function setupGameBoard(matrix){
    gameBoard.innerHTML = '';
    for (let i = 0; i < 4; i++){ 
      const row = gameBoard.insertRow();
      for (let j = 0; j < 4; j++){
        const cell = row.insertCell();
        cell.innerHTML = matrix[i][j] > 0 ? matrix[i][j] : '';
      }
    }
  }

  function getInitialGameMatrix() {
    const matrix = Array.from({length: 4}, () => Array(4).fill(0)); 
    let available = matrix.reduce((list, row, i) => row.reduce((list, cell, j) => cell ? list : [...list, [i, j]], list), [])
    if (available.length == 0)
      return matrix;
    let [row, col] = available[Math.floor(Math.random() * available.length)];
    matrix[row][col] = Math.random() < 0.9 ? 2 : 4;
    return matrix;
  }

  function move(numberList) {
    numberList = mergeTiles(numberList);
    const hasMoved = numberList.reduce((hasMoved, num, i, newNumberList) => {
      if (num) {
        let currentPos = i;
        while (currentPos - 1 >= 0 && newNumberList[currentPos - 1] === 0) {
          newNumberList[currentPos - 1] = num;
          newNumberList[currentPos] = 0;
          currentPos--;
          hasMoved = true;
        }
      }
      return hasMoved;
    }, false);

    return { numberList, hasMoved };
  }

  function mergeTiles(numberList) {
    for (let i = 0; i < numberList.length - 1; i++) {
      if (numberList[i] && numberList[i] === numberList[i + 1]) {
        numberList[i] *= 2;
        numberList[i + 1] = 0;
      }
    }
    return numberList;
  }

  // The rest of the code remains the same.
  // ...
})();