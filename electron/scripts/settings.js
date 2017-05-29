const settings = require('electron-settings')


function setSettingFromForm() {
    let forms = document.getElementsByTagName('form')
    for (let form = 0; form < forms.length; form++) {
        if (forms[form].hasAttribute("id")) {
            pref = forms[form].id.split("_form")[0]
            val = document.getElementById(forms[form].id + "_input").value
            setSetting(pref, val)
        }
    }
}

function setSetting(key, val) {
    settings.set(key, val);
}

function getSetting(key) {
    let curr = settings.get(key);
    if (curr == undefined) {
        curr = "none";
        setSetting(key, curr);
    }
    // capitalize first letter
    return curr.charAt(0).toUpperCase() + curr.slice(1);
}

function updateCurrentSetting() {
    let current = document.getElementsByClassName('currentSetting');
    for (let elem = 0; elem < current.length; elem++) {
        current[elem].value = getSetting(current[elem].name);
    }
}

function getPreferences() {
    let prefs = document.getElementsByName("preference");
    let ret = [];
    for (let select = 0; select < prefs.length; select++) {
        ret.push(document.getElementById(prefs[select].id));
    }
    return ret;
}

function getButtons() {
    let btns = document.getElementsByTagName('button');
    ret = [];
    for (let i = 0; i < btns.length; i++) {
        ret.push(document.getElementById(btns[i].id));
    }
    return ret;
}

window.onload = function() {
    let btns = getButtons();
    let prefs = getPreferences();
    for (let btn of btns) {
        btn.onclick = function () {
            document.getElementById(btn.id.split('_btn')[0]).classList.toggle('show')
        }
    }
    for (let pref of prefs) {
        pref.onchange = function () {
            // value of options in select tag must have format "key,val"
            let key = pref.id;
            let val = pref.value;
            setSetting(key, val);
            updateCurrentSetting();
        }
        updateCurrentSetting();
    }
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
