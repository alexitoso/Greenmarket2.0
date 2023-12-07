// logout_timer.js

let inactivityTime = 300000; // 5 minutos en milisegundos
let timeout;

function startTimer() {
  timeout = setTimeout(logout, inactivityTime);
}

function resetTimer() {
  clearTimeout(timeout);
  startTimer();
}

function logout() {
  // Realizar una solicitud al servidor para cerrar la sesión
  window.location.href = '/cerrarsesion'; // o la URL de tu vista de cierre de sesión
}

document.onmousemove = resetTimer;
document.onkeypress = resetTimer;

startTimer();
