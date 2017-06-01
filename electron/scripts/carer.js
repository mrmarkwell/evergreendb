const settings = require('electron-settings');

// global var for table entry data
let g_carer_table_entries = [];
const g_base_url = "http://127.0.0.1:5000";

// log to console if in debug mode
function d_log(record) {
    let in_debug_mode = settings.get('debug')
    if (in_debug_mode) {
        console.log(record);
    }
}

function TableElements() {
    return {
        caregiver_id: null,
        caregiver_english_name: null,
        caregiver_chinese_name: null,
        caregiver_pinyin_name: null,
        child_caregiver_start_date: null,
        child_caregiver_end_date: null,
        child_caregiver_note: null
    }
}

// Function to construct a TableElements object and return it.
function populateCarerTableElements(jdata) {
    let tes = [];
    for (let record of jdata) {
        let te = new TableElements();
        for (let prop in te) {
            te[prop] = record.hasOwnProperty(prop) ? record[prop] : null;
        }
        te.checkboxFuncKey = "exampleCheckboxFunction";
        te.href = "child.html?id=" + record.child_id
        tes.push(te);
    }
    return tes;
}

// Just an example to show off that a function can be called when you check the box.
// This should be used to end the child carer relationship, i.e. set the end date
function exampleCheckboxFunction(element, idx) {
    let checkedText = element.checked ? "CHECKED" : "UNCHECKED";
    alert("You " + checkedText + " the checkbox for row " + idx + " which is the row with child " + g_carer_table_entries[idx].child_english_name + " who has ID " + g_carer_table_carerentries[idx].child_id);
}

function constructCarerTable() {
    let headers = [
        "", "",         // edit link and checkbox respectively
        "English Name", "Chinese Name",
        "Pinyin Name", "Start Date",
        "End Date", "Note"
    ];
    let columnTypes = [
        columnTypeEnum.editFormLink, columnTypeEnum.checkboxFunc,
        columnTypeEnum.text, columnTypeEnum.text,
        columnTypeEnum.text, columnTypeEnum.text,
        columnTypeEnum.text, columnTypeEnum.text
    ];
    let fieldNames = [
        "href", "checkboxFuncKey",
        "caregiver_english_name", "caregiver_chinese_name",
        "caregiver_pinyin_name", "child_caregiver_start_date",
        "child_caregiver_end_date", "child_caregiver_note"
    ];
    let columnData = new ColumnData(headers, columnTypes, fieldNames);
    let tdata = new TableData("carer_table", columnData, g_carer_table_entries);
    generateTable(tdata);
}

// Main entry point. Do all the initial REST calls and get all the data.
// Construct the table.
function initializeCarerTable(child_id) {
    const caregiver_url = g_base_url + "/entity/child,child_caregiver,caregiver?child_id=" + child_id

    makeRequest({
        method: "GET",
        url: caregiver_url,
        responseType: "json"
    }).then(function (datums) {
        let tes = populateCarerTableElements(datums);
        g_carer_table_entries = g_carer_table_entries.concat(tes);
        // sort g_carer_table_entries by child_caregiver_end_date, most recent to least recent
        g_carer_table_entries.sort(function(a, b) {
            // Turn your strings into dates, and then subtract them
            // to get a value that is either negative, positive, or zero.
            // make sure empty end date ends up at the top
            if (a.child_caregiver_end_date == null) {
                return -1
            } else if (b.child_caregiver_end_date == null) {
                return 1
            } else {
                return new Date(b.child_caregiver_end_date) - new Date(a.child_caregiver_end_date);
            }
        });
        constructCarerTable();
    }).catch(function (err) {
        console.error("Error getting data from caregiver table", err);
    });
}

function makeNewCaregiver(child_id) {
    let caregiver_english_name = document.getElementById("caregiver_english_name_new").value;
    let caregiver_chinese_name = document.getElementById("caregiver_chinese_name_new").value;
    let caregiver_pinyin_name = document.getElementById("caregiver_pinyin_name_new").value;
    let child_caregiver_start_date = document.getElementById("child_caregiver_start_date_new").value;
    let child_caregiver_end_date = document.getElementById("child_caregiver_end_date_new").value;
    let child_caregiver_note = document.getElementById("child_caregiver_note_new").value;
    makeRequest({
        method: "POST",
        url: g_base_url + "/entity/caregiver",
        headers: {"Content-Type": "application/json"},
        responseType: "json",
        params: JSON.stringify({
            "caregiver_english_name": caregiver_english_name,
            "caregiver_chinese_name": caregiver_chinese_name,
            "caregiver_pinyin_name": caregiver_pinyin_name
        })
    }).then(function (datums) {
        d_log("I got the data!");
        d_log("DATUMS: " + datums)
        let caregiver_id = datums.id;
        makeRequest({
            method: "POST",
            url: g_base_url + "/entity/child_caregiver",
            headers: {"Content-Type": "application/json"},
            responseType: "json",
            params: JSON.stringify({
                "child_id": child_id,
                "caregiver_id": caregiver_id,
                "child_caregiver_start_date": child_caregiver_start_date,
                "child_caregiver_end_date": child_caregiver_end_date,
                "child_caregiver_note": child_caregiver_note
            })
        });
    }).catch(function (err) {
        console.error('Error posting data: ' + err.statusText);
    });
}
