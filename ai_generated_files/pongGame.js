// Create canvas and context
let canvas = document.querySelector("#pongGame");
const ctx = canvas.getContext('2d');

// Create the pong paddle
const paddleWidth = 50, paddleHeight = 10;
let paddleSpeed = 2;
let paddleX = canvas.width / 2;

//Create the pong ball
let x = canvas.width / 2;
let y = canvas.height - 30;
let ballRadius = 10;
let dx = 2;
let dy = -2;

//Draw paddles
function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "#00FFFF";
    ctx.fill();
    ctx.closePath();
}

//Draw balls
function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI*2);
    ctx.fillStyle = "#00FFFF";
    ctx.fill();
    ctx.closePath();
}

//Move the paddle
let rightPressed = false;
let leftPressed = false;
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

// Key down handler
function keyDownHandler(e) {
    if(e.keyCode == 39) rightPressed = true;
    else if(e.keyCode == 37) leftPressed = true;
}

// Key up handler
function keyUpHandler(e) {
    if(e.keyCode == 39) rightPressed = false;
    else if(e.keyCode == 37) leftPressed = false;
}

//Draw the objects
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    drawPaddle();

    if(rightPressed && paddleX < canvas.width - paddleWidth) paddleX += paddleSpeed;
    else if(leftPressed && paddleX > 0) paddleX -= paddleSpeed;

    if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) dx = -dx;
    if(y + dy < ballRadius) dy = -dy;
    else if(y + dy > canvas.height-ballRadius) {
        if(x > paddleX && x < paddleX + paddleWidth) dy = -dy;
        else {
            alert("GAME OVER!!");
            document.location.reload();
        }
    }
    x += dx;
    y += dy;
}

setInterval(draw, 10);