"use strict";

let flagged_notes = {
    // global var for table entry data
    table_entries: [],

    // Sets for the filter dropdowns
    child_name_set: new Set(),
    carer_name_set: new Set(),

    // Map for note type to note flag name
    note_flag_map: {
        General: "child_note_flag",
        Assessment: "child_assessment_note_flag",
        Partner: "child_partner_note_flag"
    }
}


// Class TableElements. Used to collect the elements needed in the table.
function TableElements() {
    return {
        child_english_name: null,
        child_chinese_name: null,
        child_pinyin_name: null,
        child_id: null,
        caregiver_english_name: null,
        caregiver_chinese_name: null,
        caregiver_pinyin_name: null,
        caregiver_id: null,
        note_type: null,
        id: null,
        note: null,
        href: null,
        flag: null,
        checkboxFuncKey: null // DELETE THIS
    }
}

// Populate all the options for the filter dropdowns
function setFilterOptions() {
    for (let record of flagged_notes.table_entries) {
        flagged_notes.child_name_set.add(record.child_english_name);
        flagged_notes.carer_name_set.add(record.caregiver_english_name);
    }
    let child_select = document.getElementById("child_select")
    for (let child_name of flagged_notes.child_name_set) {
        child_select.options[child_select.options.length] = new Option(child_name, child_name);
    }
    let caregiver_select = document.getElementById("caregiver_select")
    for (let caregiver_name of flagged_notes.carer_name_set) {
        caregiver_select.options[caregiver_select.options.length] = new Option(caregiver_name, caregiver_name);
    }
}

// Function to construct a TableElements object and return it.
function populateTableElements(jdata, note_type) {
    let tes = [];
    let note_tab_map = {
        General: "notes",
        Assessment: "assessment",
        Partner: "partnership"
    }
    let note_name_map = {
        General: "child_note",
        Assessment: "child_assessment_note",
        Partner: "child_partner_note"
    }
    console.log(jdata);
    for (let record of jdata) {
        //console.log(record);
        let te = new TableElements();

        for (let prop in te) {
            te[prop] = record.hasOwnProperty(prop) ? record[prop] : null;
        }
        te.note_type = note_type;
        let note_name = note_name_map[note_type];
        let tab_name = note_tab_map[note_type];
        let flag_name = flagged_notes.note_flag_map[note_type];
        te.note = record[note_name];
        te.href = "child.html?id=" + record.child_id + "#childTab-" + tab_name;
        te.flag = record[flag_name];
        te.checkboxFuncKey = "editFlag";
        //console.log(te);
        tes.push(te);
    }
    return tes;
}

// Just an example to show off that a function can be called when you check the box.
function editFlag(element, idx, entry) {
    const settings = require('electron-settings')
    let base_url = settings.get('url')
    let flag_set_val = element.checked ? true : false;
    let note_flag_name = flagged_notes.note_flag_map[entry.note_type];
    let body = {};
    body[note_flag_name] = flag_set_val;
    let table_name_map = {
        General: "child_note",
        Assessment: "child_assessment",
        Partner: "child_partner"
    }
    let url = base_url + "entity/" + table_name_map[entry.note_type] + "?id=" + entry.id;
    makeRequest({
        method: "PUT",
        url: url,
        headers: { "Content-Type": "application/json" },
        responseType: "json",
        params: JSON.stringify(body)
    }).then(function (datums) {
        console.log("Succeeded in unflagging note!");
    }).catch(function (err) {
        console.error("Error unsetting flag!", err);
    });
}

// TableEntry data is collected - now build the table itself.
function constructTable() {
    let headers = ["", "Flag", "Note Type",
        "Child", "Caregiver", "Note"];
    let columnTypes = [columnTypeEnum.viewDetailLink,
    columnTypeEnum.checkboxFunc,
    columnTypeEnum.text,
    columnTypeEnum.text,
    columnTypeEnum.text,
    columnTypeEnum.text];
    let fieldNames = ["href", "checkboxFuncKey", "note_type",
        "child_english_name", "caregiver_english_name", "note"];
    let columnData = new ColumnData(headers, columnTypes, fieldNames);
    let checkDecision = function(row_obj) { return row_obj.flag == 1 }
    let tdata = new TableData("flagged_notes_table", columnData, flagged_notes.table_entries, checkDecision);
    generateTable(tdata);
}

// Main entry point. Do all the initial REST calls and get all the data.
// Construct the table.
function initializeTable() {
    const settings = require('electron-settings')
    let base_url = settings.get('url')
    const child_note_url = base_url + "entity/child,child_caregiver,caregiver,child_note?child_note_flag=1";
    const child_assessment_url = base_url + "entity/child,child_caregiver,caregiver,child_assessment?child_assessment_note_flag=1"
    const child_partner_url = base_url + "entity/child,child_caregiver,caregiver,child_partner?child_partner_note_flag=1"


    // decrements when each request succeeds so final request can call next step.
    let requests_remaining = 3;
    let table_names = ["child_note", "child_assessment", "child_partner"];
    let note_types = ["General", "Assessment", "Partner"];
    let urls = [child_note_url, child_assessment_url, child_partner_url];
    // Get the child_note data

    for (let i = 0; i < table_names.length; i++) {
        makeRequest({
            method: "GET",
            url: urls[i]
        }).then(function (datums) {
            //console.log("I got the data!");
            let jdata = JSON.parse(datums);
            let tes = populateTableElements(jdata, note_types[i]);
            flagged_notes.table_entries = flagged_notes.table_entries.concat(tes);
            requests_remaining--;
            if (requests_remaining === 0) {
                setFilterOptions();
                constructTable();
            }
        }).catch(function (err) {
            console.error('Error getting data from ' + table_names[i], err);
        });
    }
}

// Result of a button click on the "Apply Filter" button
// Applies the selected filter to the table by hiding the undesired rows.
function filterTable() {
    let table = document.getElementById("flagged_notes_table");
    let tbody = table.getElementsByTagName("tbody")[0];
    let selected_child = document.getElementById("child_select").value;
    let selected_caregiver = document.getElementById("caregiver_select").value;
    for (let row of tbody.rows) {
        let child_name = row.cells[3].innerHTML;
        let caregiver_name = row.cells[4].innerHTML;
        if (selected_child === "All Children" || child_name === selected_child) {
            row.style.display = "";
        } else {
            row.style.display = "none";
            // If it is not the selected child, no need to check caregivers.
            continue;
        }
        if (selected_caregiver === "All Caregivers" || caregiver_name === selected_caregiver) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
}

