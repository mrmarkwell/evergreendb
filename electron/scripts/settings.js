const settings = require('electron-settings')


function setSetting(key, val) {
    settings.set(key, val);
}

function getSetting(key) {
    let curr = settings.get(key);
    if (curr == undefined) {
        console.log("setting key " + key);
        console.log("to none")
        curr = "none"
        setSetting(key, curr)
    }
    // capitalize first letter
    return curr.charAt(0).toUpperCase() + curr.slice(1)
}

function updateCurrentSetting() {
    let current = document.getElementById('currentSetting');
    current.value = getSetting(current.name);
}

window.onload = function() {
    document.getElementById("myDropdown").onchange = function () {
        // value of options in select tag must have format "key,val"
        let keyval = this.value.split(",");
        let key = keyval[0];
        let val = keyval[1];
        setSetting(key, val);
        updateCurrentSetting();
    }
    updateCurrentSetting();
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn') && !event.target.matches('.dropdown-content')) {
    let dropdowns = document.getElementsByClassName("dropdown-content");
    let i;
    for (i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
