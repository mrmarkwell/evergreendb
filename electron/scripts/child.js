var BASE_URL = "http://127.0.0.1:5000/"; // change this to get from settings later

function fillChildTabData(json) {
	// Make sure only one child is returned and get that child from array
	if (json.length != 1) {
		console.log("Expected one child to be returned got ",json.length);
		return;
	}
	child_data = json[0];

	// Fill text fields that match name of column
	fillNormalFields(child_data);
	// Fill age
	fillAge(child_data.birth_date)
	// Fill gender
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
	var med_cond_req_settings = {
		"url": BASE_URL + "entity/medical_condition",
		"async": true,"method": "GET","crossDomain": true,"headers": {"cache-control": "no-cache",}
	};
	var child_med_cond_req_settings = {
		"url": BASE_URL + "entity/child_medical_condition?"+jQuery.param({"child_id":child_id}),
		"async": true,"method": "GET","crossDomain": true,"headers": {"cache-control": "no-cache",}
	};
	
	jQuery.when(
		jQuery.ajax(med_cond_req_settings),
		jQuery.ajax(child_med_cond_req_settings)
	).then(function(a1,a2) {fillMedicalConditions(a1[0],a2[0])});
}
function fillMedicalConditions(all_conditions, child_conditions) {
	var select_box = document.getElementById('medical_condition');
	for (var i in all_conditions) {
		var opt = document.createElement('option');
		opt.innerHTML = all_conditions[i].medical_condition_english_name;
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

function fillMedicationDropdown(json) {
	var select_box = document.getElementById('medication_new');
	let opt = document.createElement('option');
	opt.value = "";
	select_box.options.add(opt);
	for (let i=0; i<json.length; i++) {
		let opt = document.createElement('option');
		opt.value = json[i].id;
		opt.innerHTML = json[i].medication_english_name;
		select_box.options.add(opt)
	}
	jQuery(".chosen-select").trigger('chosen:updated'); // Needed because chosen-select doesn't update ui automatically like regular select
}
function fillMedicationTable(child_medications) {
	let medication_table = document.getElementById('child_medication_table');
	child_medications.sort(function(a,b) {
		return (a.child_medication_end_date > b.child_medication_end_date) ? 1 : ((a.child_medication_end_date < b.child_medication_end_date) ? -1 : 0);
	}); 
	for (let i=0; i<child_medications.length; i++) {
		let row = document.createElement('TR');
		let child_med_id = child_medications[i].id; 
		// medication name
		let table_str = '<td>' + child_medications[i].medication_english_name + '</td>';
		// dosages
		table_str += '<td>' + child_medications[i].dosage1 + '</td><td>' + child_medications[i].dosage2 + '</td><td>' + child_medications[i].dosage3 + '</td>';
		// start/stop dates
		table_str += '<td>' + child_medications[i].child_medication_start_date + '</td>';
		table_str += '<td><input type="text" class="datepicker" id="medication_end_date_' + child_med_id + '" value="' + child_medications[i].child_medication_end_date + '" size="9"></td>';
		// ended checkbox
		table_str += '<td><input type="checkbox" id="medication_finished_' + child_med_id + '" onchange=\'endChildMedication("' + child_med_id + '",this)\'';
		let today = new Date();
		let end_date = child_medications[i].child_medication_end_date;
		if (end_date !== null) {
			end_date = jQuery.datepicker.parseDate("yy-mm-dd",end_date);
			if (end_date <= today) {
				table_str += ' checked';
				//TODO: Grey out row
			}
		}
		table_str += '></td>';
		row.innerHTML = table_str;
		medication_table.appendChild(row);
	}
	jQuery(".datepicker").datepicker({dateFormat: "yy-mm-dd"});
}
function endChildMedication(child_med_id, checkbox) {
	console.log(child_med_id)
	if (checkbox.checked) {
		var now = new Date();
	} else {
		var now = null;
	}
	jQuery("#medication_end_date_" + child_med_id).datepicker("setDate",now);
}
function addChildMedication() {
	// Set values
	let e = document.getElementById('medication_new');
	let child_medication_info = {
		"medication_id": Number(e.options[e.selectedIndex].value),
		"dosage1": Number(document.getElementById('dosage1_new').value),
		"dosage2": Number(document.getElementById('dosage2_new').value),
		"dosage3": Number(document.getElementById('dosage3_new').value),
		"child_medication_start_date": document.getElementById('medication_start_date_new').value,
		"child_id": Number(getParameterByName("id")) // From libs.js, no namespaces is annoying
	};
	let end_date = document.getElementById('medication_end_date_new').value;
	if (end_date != "") { // Only add end_date if provided
		child_medication_info.child_medication_end_date = end_date;
	}
	// Check values
	if (child_medication_info.medication_id === 0) {window.alert("Select a medication first!"); return;}
	if (child_medication_info.dosage1 === 0 && child_medication_info.dosage2 === 0 && child_medication_info.dosage3 === 0) {window.alert("At least one dosage must be not 0!"); return;}
	if (child_medication_info.dosage1 < 0 || child_medication_info.dosage2 < 0 || child_medication_info.dosage3 < 0) {window.alert("Dosage cannot be negative!"); return;}
	if (child_medication_info.child_medication_start_date === "") {window.alert("Select a start date first!"); return;}
	console.log(child_medication_info);
	// Send POST
	restPost('entity/child_medication',child_medication_info,function(json) {location.reload();});
}
