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

function requestMedicalConditions(child_id) {
	var med_cond_settings = {
		"url": "http://127.0.0.1:5000/entity/medical_condition",
		"async": true,"method": "GET","crossDomain": true,"headers": {"cache-control": "no-cache",}
	};
	var child_med_cond_settings = {
		"url": "http://127.0.0.1:5000/entity/child_medical_condition?"+jQuery.param({"child_id":child_id}),
		"async": true,"method": "GET","crossDomain": true,"headers": {"cache-control": "no-cache",}
	};
	
	jQuery.when(
		jQuery.ajax(med_cond_settings),
		jQuery.ajax(child_med_cond_settings)
	).then(function(a1,a2) {fillMedicalConditions(a1[0],a2[0])});
}
function fillMedicalConditions(all_conditions, child_conditions) {
	console.log(all_conditions,child_conditions);
	var select_box = document.getElementById('medical_condition');
	for (var i in all_conditions) {
		var opt = document.createElement('option');
		opt.innerHTML = all_conditions[i].medical_condition_english_name;;
		opt.value = all_conditions[i].id;
		for (var j in child_conditions) {
			if (all_conditions[i].id === child_conditions[j].medical_condition_id) {
				opt.selected = true;
			}
		}
		select_box.options.add(opt);
	}
	jQuery(".chosen-select").trigger('chosen:updated'); // Needed because chosen-select doesn't update ui automatically like regular select
}
