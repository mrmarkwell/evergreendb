function getParameterByName(name, url) {
	var regex = new RegExp("[?&]" + name + "=(.*)(&|$|#)");
	results = regex.exec(window.location.href);
	if (!url) url = window.location.href;
	if (!results) return null;
	if (!results[1]) return '';
	return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function getTabData(entity, child_id) {
	var BASE_URL = "http://127.0.0.1:5000/";
	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;
	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			fillChildTabData(JSON.parse(this.responseText));
		}
	});
	var query = jQuery.param({"id":child_id});
	var url = BASE_URL + "entity/" + entity + "?" + query;
	xhr.open("GET", url);
	xhr.send(null);
}

function fillChildTabData(json) {
	// Make sure only one child is returned and get that child from array
	if (json.length != 1) {
		console.log("Expected one child to be returned got ",json.length);
		return;
	}
	child_data = json[0];

	fillNormalFields(child_data); // Fills text fields that match name of column

	// Fill special fields
	// age
	fillAge(child_data.birth_date)
	// gender
	if (child_data.sex == "M") {
		document.getElementById("sex_m").checked = true;
	} else if (child_data.sex = "F") {
		document.getElementById("sex_f").checked = true;
	} 
}

function fillNormalFields(jsonDict) {
	for (var key in jsonDict) {
		var obj = document.getElementById(key);
		if (obj != null) {
			obj.value = jsonDict[key];
		}
	}
}

function fillAge(birthdate_str) {
	var today = new Date();
	var birthdate = jQuery.datepicker.parseDate("yy-mm-dd",birthdate_str);
	var age = today.getFullYear() - birthdate.getFullYear();
	var m = today.getMonth() - birthdate.getMonth();
	if (m < 0 || (m === 0 && today.getDate() < birthdate.getDate())) {
		age--;
	}
	document.getElementById('age').innerHTML = age;
}
