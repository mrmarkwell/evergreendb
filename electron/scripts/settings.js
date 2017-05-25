const settings = require('electron-settings')


function setSetting(key, value) {
    settings.set(key, value)
}

window.onload = function() {
    document.getElementById("myDropdown").onchange = function () {
        // value of options in select tag must have format "key,val"
        var keyval = this.value
        var key = keyval[0]
        var val = keyval[1]
        setSetting(key, val)
    }
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}