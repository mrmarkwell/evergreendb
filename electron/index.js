
// Main javascript file for home page.


// Black majick below: since we're requiring main.js, all
// the functions in main.js that are "exported" can be called
// in this file now. We want this because we want the main thread,
// not the render thread, to do the work of opening the new \
// window (among other things).
const remote = require('electron').remote
const main = remote.require('./main.js')

let button = document.createElement('button')
button.textContent = 'Open Flagged Notes'
button.addEventListener('click', () => {
    main.openWindow()
}, false)
document.body.appendChild(button)

