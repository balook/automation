const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const paddleWidth = 10;
const paddleHeight = 100;
const ballRadius = 10;

let paddle1Y = (canvas.height - paddleHeight) / 2;
let paddle2Y = (canvas.height - paddleHeight) / 2;

let ballX = canvas.width / 2;
let ballY = canvas.height / 2;
let ballSpeedX = 5;
let ballSpeedY = 5;

const paddleSpeed = 7;

let upArrowPressed = false;
let downArrowPressed = false;
let wPressed = false;
let sPressed = false;

document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);

function keyDownHandler(e) {
    if (e.key === 'Up' || e.key === 'ArrowUp') {
        upArrowPressed = true;
    } else if (e.key === 'Down' || e.key === 'ArrowDown') {
        downArrowPressed = true;
    } else if (e.key === 'w') {
        wPressed = true;
    } else if (e.key === 's') {
        sPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === 'Up' || e.key === 'ArrowUp') {
        upArrowPressed = false;
    } else if (e.key === 'Down' || e.key === 'ArrowDown') {
        downArrowPressed = false;
    } else if (e.key === 'w') {
        wPressed = false;
    } else if (e.key === 's') {
        sPressed = false;
    }
}

function drawPaddle(x, y) {
    ctx.fillStyle = '#000';
    ctx.fillRect(x, y, paddleWidth, paddleHeight);
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#000';
    ctx.fill();
    ctx.closePath();
}

function movePaddles() {
    if (upArrowPressed && paddle2Y > 0) {
        paddle2Y -= paddleSpeed;
    } else if (downArrowPressed && paddle2Y < canvas.height - paddleHeight) {
        paddle2Y += paddleSpeed;
    }

    if (wPressed && paddle1Y > 0) {
        paddle1Y -= paddleSpeed;
    } else if (sPressed && paddle1Y < canvas.height - paddleHeight) {
        paddle1Y += paddleSpeed;
    }
}

function moveBall() {
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    if (ballY + ballRadius > canvas.height || ballY - ballRadius < 0) {
        ballSpeedY = -ballSpeedY;
    }

    if (ballX + ballRadius > canvas.width) {
        if (ballY > paddle2Y && ballY < paddle2Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
        } else {
            resetBall();
        }
    } else if (ballX - ballRadius < 0) {
        if (ballY > paddle1Y && ballY < paddle1Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
        } else {
            resetBall();
        }
    }
}

function resetBall() {
    ballX = canvas.width / 2;
    ballY = canvas.height / 2;
    ballSpeedX = -ballSpeedX;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPaddle(0, paddle1Y);
    drawPaddle(canvas.width - paddleWidth, paddle2Y);
    drawBall();
    movePaddles();
    moveBall();
    requestAnimationFrame(draw);
}

draw();
