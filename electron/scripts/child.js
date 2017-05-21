function getTabData(entity, child_id) {
	var data = null;

	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			console.log(this.responseText);
		}
	});

	xhr.open("GET", "http://127.0.0.1:5000/entity/child?id=2");

	xhr.send(data);
}
