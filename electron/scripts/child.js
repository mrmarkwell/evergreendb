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

function fillMedicalConditionsDropdown(json) {

}
