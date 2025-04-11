function updateTimer()
{
var hours = parseInt(document.getElementById('countdown').textContent.split(':')[0]);
var minutes = parseInt(document.getElementById('countdown').textContent.split(':')[1]);
var seconds = parseInt(document.getElementById('countdown').textContent.split(':')[2]);

if (seconds > 0) {
  seconds--;
}
else {
  if (minutes > 0) {
    minutes--;
    seconds = 59;
  }
  else {
    if (hours > 0) {
      hours--;
      minutes=59;
      seconds=59;
    } else {
      // timer has reached end
    }
  }
}

// Update timer display
document.getElementById("countdown").textContent = (hours < 10 ? '0' : '') + hours + ':' +
 (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
} // end function
// update timer every second
setInterval(updateTimer, 1000);