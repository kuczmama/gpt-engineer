const canvas = document.getElementById("gameCanvas");
const context = canvas.getContext("2d");
const ballRadius = 10;
const paddleHeight = 10;
const paddleWidth = 75;
const brickRowCount = 3;
const brickColumnCount = 5;
const brickWidth = 75;
const brickHeight = 20;
const brickPadding = 10;
const brickOffsetTop = 30;
const brickOffsetLeft = 30;
let x = canvas.width / 2;
let y = canvas.height - 30;
let ballSpeedX = 2;
let ballSpeedY = -2;
let paddleX = (canvas.width - paddleWidth) / 2;
let isRightPressed = false;
let isLeftPressed = false;
let gameScore = 0;
let lives = 3;

const bricks = [];
for (let column = 0; column < brickColumnCount; column++) {
  bricks[column] = [];
  for (let row = 0; row < brickRowCount; row++) {
    bricks[column][row] = { x: 0, y: 0, status: 1 };
  }
}

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
document.addEventListener("mousemove", mouseMoveHandler, false);

function drawBall() {
  context.beginPath();
  context.arc(x, y, ballRadius, 0, Math.PI * 2);
  context.fillStyle = "#0095DD";
  context.fill();
  context.closePath();
}

function drawPaddle() {
  context.beginPath();
  context.rect(
    paddleX,
    canvas.height - paddleHeight,
    paddleWidth,
    paddleHeight
  );
  context.fillStyle = "#0095DD";
  context.fill();
  context.closePath();
}

function drawBricks() {
  for (let column = 0; column < brickColumnCount; column++) {
    for (let row = 0; row < brickRowCount; row++) {
      if (bricks[column][row].status === 1) {
        const brickX = column * (brickWidth + brickPadding) + brickOffsetLeft;
        const brickY = row * (brickHeight + brickPadding) + brickOffsetTop;
        bricks[column][row].x = brickX;
        bricks[column][row].y = brickY;
        context.beginPath();
        context.rect(brickX, brickY, brickWidth, brickHeight);
        context.fillStyle = "#0095DD";
        context.fill();
        context.closePath();
      }
    }
  }
}

function drawScore() {
  context.font = "16px Arial";
  context.fillStyle = "#0095DD";
  context.fillText("Score: " + gameScore, 8, 20);
}

function drawLives() {
  context.font = "16px Arial";
  context.fillStyle = "#0095DD";
  context.fillText("Lives: " + lives, canvas.width - 65, 20);
}

function keyDownHandler(event) {
  if (event.key === "Right" || event.key === "ArrowRight") {
    isRightPressed = true;
  } else if (event.key === "Left" || event.key === "ArrowLeft") {
    isLeftPressed = true;
  }
}

function keyUpHandler(event) {
  if (event.key === "Right" || event.key === "ArrowRight") {
    isRightPressed = false;
  } else if (event.key === "Left" || event.key === "ArrowLeft") {
    isLeftPressed = false;
  }
}

function mouseMoveHandler(event) {
  const relativeX = event.clientX - canvas.offsetLeft;
  if (relativeX > 0 && relativeX < canvas.width) {
    paddleX = relativeX - paddleWidth / 2;
  }
}

function collisionDetection() {
  for (let column = 0; column < brickColumnCount; column++) {
    for (let row = 0; row < brickRowCount; row++) {
      const brick = bricks[column][row];
      if (brick.status === 1) {
        if (
          x > brick.x &&
          x < brick.x + brickWidth &&
          y > brick.y &&
          y < brick.y + brickHeight
        ) {
          ballSpeedY = -ballSpeedY;
          brick.status = 0;
          gameScore++;
          if (gameScore === brickRowCount * brickColumnCount) {
            alert("YOU WIN, CONGRATULATIONS!");
            document.location.reload();
          }
        }
      }
    }
  }
}

function draw() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  drawBricks();
  drawBall();
  drawPaddle();
  drawScore();
  drawLives();
  collisionDetection();

  if (x + ballSpeedX > canvas.width - ballRadius || x + ballSpeedX < ballRadius) {
    ballSpeedX = -ballSpeedX;
  }
  if (y + ballSpeedY < ballRadius) {
    ballSpeedY = -ballSpeedY;
  } else if (y + ballSpeedY > canvas.height - ballRadius) {
    if (x > paddleX && x < paddleX + paddleWidth) {
      ballSpeedY = -ballSpeedY;
    } else {
      lives--;
      if (!lives) {
        alert("GAME OVER");
        document.location.reload();
      } else {
        x = canvas.width / 2;
        y = canvas.height - 30;
        ballSpeedX = 2;
        ballSpeedY = -2;
        paddleX = (canvas.width - paddleWidth) / 2;
      }
    }
  }

  if (isRightPressed && paddleX < canvas.width - paddleWidth) {
    paddleX += 7;
  } else if (isLeftPressed && paddleX > 0) {
    paddleX -= 7;
  }

  x += ballSpeedX;
  y += ballSpeedY;

  requestAnimationFrame(draw);
}

draw();