var BASE_URL = "http://127.0.0.1:5000/";

// Get the query parameters of the current page (not visable in electron)
function getParameterByName(name, url) {
	var regex = new RegExp("[?&]" + name + "=([^&#]*)(&|$|#)");
	results = regex.exec(window.location.href);
	if (!url) url = window.location.href;
	if (!results) return null;
	if (!results[1]) return '';
	return decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Run a REST GET with callback
function restGet(relative_url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;
	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			callback(JSON.parse(this.responseText));
		}
	});
	var url = BASE_URL + relative_url
	xhr.open("GET", url);
	xhr.send(null);
}
