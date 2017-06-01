var BASE_URL = "http://127.0.0.1:5000/";

// Get the query parameters of the current page (not visable in electron)
function getParameterByName(name, url) {
	var regex = new RegExp("[?&]" + name + "=([^&#]*)(&|$|#)");
	if (!url) url = window.location.href;
	results = regex.exec(url);
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
			if (this.status >= 300) {
				badRequest(this.status, JSON.parse(this.responseText));
			} else {
				callback(JSON.parse(this.responseText));
			}
		}
	});
	xhr.open("GET", BASE_URL + relative_url);
	xhr.setRequestHeader("cache-control", "no-cache");
	xhr.send(null);
}

function restPost(relative_url, body, callback) {
	let data = JSON.stringify(body);

	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			if (this.status >= 300) {
				badRequest(this.status, JSON.parse(this.responseText));
			} else {
				callback(JSON.parse(this.responseText));
			}
		}
	});

	xhr.open("POST", BASE_URL + relative_url);
	xhr.setRequestHeader("content-type", "application/json");
	xhr.setRequestHeader("accept", "application/json");
	xhr.setRequestHeader("cache-control", "no-cache");

	xhr.send(data);
}

function restDelete(relative_url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			if (this.status >= 300) {
				badRequest(this.status, JSON.parse(this.responseText));
			} else {
				callback();
			}
		}
	});

	xhr.open("DELETE", BASE_URL + relative_url);
	xhr.setRequestHeader("content-type", "application/json");
	xhr.setRequestHeader("accept", "application/json");
	xhr.setRequestHeader("cache-control", "no-cache");

	xhr.send(null);
}

function restPut(relative_url, body, callback) {
	let data = JSON.stringify(body);

	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			if (this.status >= 300) {
				badRequest(this.status, JSON.parse(this.responseText));
			} else {
				callback(JSON.parse(this.responseText));
			}
		}
	});

	xhr.open("PUT", BASE_URL + relative_url);
	xhr.setRequestHeader("content-type", "application/json");
	xhr.setRequestHeader("accept", "application/json");
	xhr.setRequestHeader("cache-control", "no-cache");

	xhr.send(data);
}

function badRequest(ret_status, json) {
	let error_str = "";
	for (let i in json.message) {
		error_str += "Error " + ret_status + " with " + i + ":\n  " + json.message[i] + "\n";
	}
	console.log(error_str);
	window.alert(error_str);
}
