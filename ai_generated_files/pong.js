// select canvas
const canvas = document.getElementById("pong");
const context = canvas.getContext("2d");

// create the pong paddle
const paddleWidth = 50, paddleHeight = 10;
const player = { x: canvas.width / 2 - paddleWidth / 2, y: canvas.height - paddleHeight - 5, width: paddleWidth, height: paddleHeight, color: "#808080", dy: 4 };
function drawRect(x, y, width, height, color) {
    context.fillStyle = color;
    context.fillRect(x, y, width, height);
}

// create the pong ball
const ball = { x: canvas.width / 2, y: player.y - 10, radius: 10, speed: 2, dx: 2, dy: -2, color: "#808080" };
function drawCircle(x, y, radius, color) {
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2, false);
    context.closePath();
    context.fillStyle = color;
    context.fill();
}

// move the paddles
function movePaddle(paddle, upKey, downKey) {
    document.addEventListener("keydown", function(event) {
        switch(event.keyCode) {
            case upKey:
                paddle.y -= paddle.dy;
                break;
            case downKey:
                paddle.y += paddle.dy;
                break;
        }
    });
}

// move the ball
function moveBall(ball) {
    ball.x += ball.dx;
    ball.y += ball.dy;

    if(ball.y + ball.radius > canvas.height) {
        ball.y = canvas.height - ball.radius;
        ball.dy *= -1;
    }
}

// update the canvas
function update() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawRect(player.x, player.y, player.width, player.height, player.color);
    drawCircle(ball.x, ball.y, ball.radius, ball.color);
    moveBall(ball);
}

// loop
function loop() {
    update();
    if(typeof requestId !== 'undefined') cancelAnimationFrame(requestId);
    requestId = requestAnimationFrame(loop);
}
loop();