"use strict";

// global var for table entry data
let g_table_entries = [];

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
        note: null,
        href: null,
        checkboxFuncKey: null // DELETE THIS
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
        te.note = record[note_name];
        te.href = "child.html?id=" + record.child_id + "#childTab-" + tab_name;
        te.checkboxFuncKey = "exampleCheckboxFunction"; // DELETE THIS
        //console.log(te);
        tes.push(te);
    }
    return tes;
}

// Just an example to show off that a function can be called when you check the box.
function exampleCheckboxFunction(element, idx, entry) {
    let checkedText = element.checked ? "CHECKED" : "UNCHECKED";
    alert("You " + checkedText + " the checkbox for row " + idx + " which is the row with child " + entry.caregiver_english_name + " who has ID " + entry.caregiver_id);
}

// TableEntry data is collected - now build the table itself.
function constructTable() {
    let headers = ["", "EXAMPLE EDIT", "EXAMPLE CHECKBOX", "Note Type",
        "Child", "Caregiver", "Note"];
    let columnTypes = [columnTypeEnum.viewDetailLink,
    columnTypeEnum.editFormLink,
    columnTypeEnum.checkboxFunc,
    columnTypeEnum.text,
    columnTypeEnum.text,
    columnTypeEnum.text,
    columnTypeEnum.text];
    let fieldNames = ["href", "href", "checkboxFuncKey", "note_type",
        "child_english_name", "caregiver_english_name", "note"];
    let columnData = new ColumnData(headers, columnTypes, fieldNames);
    let checkDecision = function(row_json) {
        let row_obj = JSON.parse(row_json)
        if (row_obj.child_id == 1) {
            console.log(row_obj)
            return 1;
        } else {
            return 0;
        }
    }
    let tdata = new TableData("flagged_notes_table", columnData, g_table_entries, checkDecision);
    generateTable(tdata);
}

// THE OLD WAY - Leaving this here for reference. TO BE REMOVED.
//function constructTable() {
//    console.log(g_table_entries);
//    let headers = ["note_type", "child_english_name", "caregiver_english_name", "note"];
//    let tbody = document.getElementById("flagged_notes_table_body");
//    for (let entry of g_table_entries) {
//        let tr = document.createElement("tr");
//        let td = document.createElement("td");
//        let a = document.createElement("a");
//        let link_text = document.createTextNode("Go To Note");
//        a.appendChild(link_text);
//        a.title = "Go To Note";
//        a.href = entry.href;
//        td.appendChild(a);
//        tr.appendChild(td);
//        for (let header of headers) {
//            let td = document.createElement("td");
//            td.appendChild(document.createTextNode(entry[header]));
//            tr.appendChild(td);
//        }
//        tbody.appendChild(tr);
//    }
//}

// Main entry point. Do all the initial REST calls and get all the data.
// Construct the table.
function initializeTable() {
    const base_url = "http://127.0.0.1:5000";
    const child_note_url = base_url + "/entity/child,child_caregiver,caregiver,child_note?child_note_flag=1";
    const child_assessment_url = base_url + "/entity/child,child_caregiver,caregiver,child_assessment,specialist?child_assessment_note_flag=1"
    const child_partner_url = base_url + "/entity/child,child_caregiver,caregiver,child_partner,partner?child_partner_note_flag=1"

    const child_url = base_url + "/entity/child";
    const caregiver_url = base_url + "/entity/caregiver"

    makeRequest({
        method: "GET",
        url: child_url
    }).then(function (datums) {
        let jdata = JSON.parse(datums);
        let child_select = document.getElementById("child_select")
        for (let entry of jdata) {
            child_select.options[child_select.options.length] = new Option(entry.child_english_name, entry.child_english_name);
        }
    }).catch(function (err) {
        console.error("Error setting up child select dropdown!", err);
    });

    makeRequest({
        method: "GET",
        url: caregiver_url
    }).then(function (datums) {
        let jdata = JSON.parse(datums);
        let caregiver_select = document.getElementById("caregiver_select")
        for (let entry of jdata) {
            caregiver_select.options[caregiver_select.options.length] = new Option(entry.caregiver_english_name, entry.caregiver_english_name);
        }
    }).catch(function (err) {
        console.error("Error setting up caregiver select dropdown!", err);
    });


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
            g_table_entries = g_table_entries.concat(tes);
            requests_remaining--;
            if (requests_remaining === 0) {
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
    let tbody = document.getElementById("flagged_notes_table_body");
    let selected_child = document.getElementById("child_select").value;
    let selected_caregiver = document.getElementById("caregiver_select").value;
    for (let row of tbody.rows) {
        let child_name = row.cells[2].innerHTML;
        let caregiver_name = row.cells[3].innerHTML;
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

