var BASE_URL = "http://127.0.0.1:5000/"; // change this to get from settings later
var g_child_medical_conditions = [];

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

function updateMedicalHistory() {
	let data = {"medical_history": document.getElementById("medical_history").value};
	restPut('entity/child?id=' + Number(getParameterByName("id")), data, function(x) {});
}

// Medical Conditions
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
	g_child_medical_conditions = child_conditions;
}
function updateMedicalConditions() {
	let selected = jQuery('#medical_condition').chosen().val() // Get the medical condition select box, convert it to class Chosen, and get the selected values
	//Python equiv of below 3 lines:
	//  selected = [int(x) for x in selected]
	//  child_medical_cond = [x.medical_condition_id for x in g_child_medical_conditions]
	//  added = [x for x in selected if x not in child_medical_cond]
	selected = selected.map(function(x) {return Number(x);});
	let child_medical_cond = g_child_medical_conditions.map(function(x) {return x.medical_condition_id;});
	let added = selected.filter(function(x) {return !child_medical_cond.includes(x);}); 

	let to_remove = [];
	for (let i=0; i<g_child_medical_conditions.length; i++) {
		let condition = g_child_medical_conditions[i];
		if (!selected.includes(condition.medical_condition_id)) {
			to_remove.push(i);// Have to do this later or the iterator will get all messed up
			restDelete('entity/child_medical_condition?id=' + condition.id, function() {});
		}
	}
	for (let indx of to_remove) { 
		g_child_medical_conditions.splice(indx,1);
	}
	for (let itm of added) {
		let data = {"child_id": Number(getParameterByName("id")), "medical_condition_id": itm};
		restPost('entity/child_medical_condition', data, function(x) {g_child_medical_conditions.push(x);});
	}
}

// Medications
function fillMedicationDropdown(json) {
	var select_box = document.getElementById('medication_new');
	let opt = document.createElement('option');
	opt.value = "";
	select_box.options.add(opt);
	for (let element of json) {
		let opt = document.createElement('option');
		opt.value = element.id;
		opt.innerHTML = element.medication_english_name;
		select_box.options.add(opt)
	}
	jQuery(".chosen-select").trigger('chosen:updated'); // Needed because chosen-select doesn't update ui automatically like regular select
}
function fillMedicationTable(child_medications) {
	let medication_table = document.getElementById('child_medication_table');
	child_medications.sort(function(a,b) {
		let date1 = a.child_medication_end_date; let date2 = b.child_medication_end_date;
		if (date1 < date2 || (date1 !== null && date2 === null)) {return 1;}
		if (date1 > date2 || (date1 === null && date2 !== null)) {return -1;}
		return 0;
	}); 
	for (let medication of child_medications) {
		let row = document.createElement('TR');
		let child_med_id = medication.id; 
		row.id = "child_med_row_" + child_med_id;
		// medication name
		let table_str = '<td>' + medication.medication_english_name + '</td>';
		// dosages
		table_str += '<td>' + medication.dosage1 + '</td><td>' + medication.dosage2 + '</td><td>' + medication.dosage3 + '</td>';
		// start/stop dates
		table_str += '<td>' + medication.child_medication_start_date + '</td>';
		let end_date_str = (medication.child_medication_end_date === null) ? "" : medication.child_medication_end_date;
		table_str += '<td id="medication_end_date_' + child_med_id + '">' + end_date_str + '</td>';
		// ended checkbox
		table_str += '<td><input type="checkbox" id="medication_finished_' + child_med_id + '" onchange=\'endChildMedication("' + child_med_id + '",this)\'';
		let today = new Date();
		let end_date = medication.child_medication_end_date;
		if (end_date !== null) {
			end_date = jQuery.datepicker.parseDate("yy-mm-dd",end_date);
			if (end_date <= today) {
				table_str += ' checked';
				row.classList.add("grayedout");
			}
		}
		table_str += '></td>';
		row.innerHTML = table_str;
		medication_table.appendChild(row);
	}
	jQuery(".datepicker").datepicker({dateFormat: "yy-mm-dd"});
}
function endChildMedication(child_med_id, checkbox) {
	let now = null;
	let now_str = "";
	let row = document.getElementById('child_med_row_'+child_med_id);
	if (checkbox.checked) {
		now_str = jQuery.datepicker.formatDate("yy-mm-dd",new Date());
		now = now_str;
		row.classList.add("grayedout");
	} else {
		row.classList.remove("grayedout");
	}
	//let end_date_box = jQuery("#medication_end_date_" + child_med_id);
	//end_date_box.datepicker("setDate",now);
	//restPut("entity/child_medication?id="+child_med_id, {"child_medication_end_date":end_date_box[0].value}, function(x) {console.log(x);});
	document.getElementById('medication_end_date_'+child_med_id).innerHTML = now_str;
	restPut("entity/child_medication?id="+child_med_id, {"child_medication_end_date":now}, function(x) {location.reload();});
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
	// Send POST
	restPost('entity/child_medication',child_medication_info,function(json) {location.reload();});
}

// Measurements
function createMeasurementSection(measurement_types) {
	let measurements_p = document.getElementById("child_measurements");
	let language = "english";
	for (let measure_type of measurement_types) {
		let header = document.createElement('H6');
		header.innerHTML = measure_type['measurement_type_' + language + '_name'];
		let table = document.createElement('TABLE');
		table.id = 'measurement_table_type' + measure_type.id;
		restGet("entity/measurement_type,child_measurement?"+jQuery.param({"child_id":getParameterByName("id"),"measurement_type_id":measure_type.id}),
			function(json) {fillMeasurementTable(json,table.id);}
		);
		measurements_p.appendChild(header);
		measurements_p.appendChild(table);
	}
}
function fillMeasurementTable(measurements,table_id) {
	console.log(table_id,measurements);
	let headers = ["","Date","Measurement","Unit","Comments"]; // "" is edit column
	let column_types = [columnTypeEnum.editFormLink, columnTypeEnum.text,
		columnTypeEnum.text, columnTypeEnum.text, columnTypeEnum.text];
	let field_names = ['href',"child_measurement_date","child_measurement_value","units","comment"];
	let column_data = new ColumnData(headers, column_types, field_names);
	let tdata = new TableData(table_id, column_data, measurements);
	generateTable(tdata);
}
