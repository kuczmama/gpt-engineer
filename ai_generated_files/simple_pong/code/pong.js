function drawPaddle(x, y, width, height, color) {
   context.fillStyle = color;
   context.fillRect(x, y, width, height);
 }
 
 function drawBall(x, y, radius, color) {
   context.fillStyle = color;
   context.beginPath();
   context.arc(x, y, radius, 0, Math.PI * 2, false);
   context.closePath();
   context.fill();
 }
 
 function drawNet() {
   for (let i = 0; i <= canvas.height; i += 15) {
     drawPaddle(canvas.width / 2 - 1, i, 2, 10, "#FFF");
   }
 }
 
 function draw() {
   let canvas = document.getElementById("pong");
   let context = canvas.getContext("2d");
 
   // Clear the canvas
   context.clearRect(0, 0, canvas.width, canvas.height);
 
   drawPaddle(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height, leftPaddle.color);
   drawPaddle(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height, rightPaddle.color);
   drawBall(ball.x, ball.y, ball.radius, ball.color);
   drawNet();
 }
 
 function update() {
   let canvas = document.getElementById("pong");
   let context = canvas.getContext("2d");
 
   ball.x += ball.dx;
   ball.y += ball.dy;
 
   // Ball collision with the top and bottom walls
   if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
     ball.dy *= -1;
   }
 
   // Ball collision with the paddles
   if (
     ball.x - ball.radius < leftPaddle.x + leftPaddle.width &&
     ball.y + ball.radius > leftPaddle.y &&
     ball.y - ball.radius < leftPaddle.y + leftPaddle.height
   ) {
     ball.dx *= -1;
   }
 
   if (
     ball.x + ball.radius > rightPaddle.x &&
     ball.y + ball.radius > rightPaddle.y &&
     ball.y - ball.radius < rightPaddle.y + rightPaddle.height
   ) {
     ball.dx *= -1;
   }
 }
 
 function handleKeyDown(event) {
   switch (event.code) {
     case "ArrowUp":
       if (rightPaddle.y - rightPaddle.dy > 0) {
         rightPaddle.y -= rightPaddle.dy;
       }
       break;
     case "ArrowDown":
       if (rightPaddle.y + rightPaddle.dy + rightPaddle.height < canvas.height) {
         rightPaddle.y += rightPaddle.dy;
       }
       break;
     case "KeyW":
       if (leftPaddle.y - leftPaddle.dy > 0) {
         leftPaddle.y -= leftPaddle.dy;
       }
       break;
     case "KeyS":
       if (leftPaddle.y + leftPaddle.dy + leftPaddle.height < canvas.height) {
         leftPaddle.y += leftPaddle.dy;
       }
       break;
   }
 }
 
 document.addEventListener("keydown", handleKeyDown);
 
 function loop() {
   let canvas = document.getElementById("pong");
   let context = canvas.getContext("2d");
 
   update();
   draw();
   requestAnimationFrame(loop);
 }
 
 loop();