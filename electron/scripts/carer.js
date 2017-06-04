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
    let hist_tes = [];
    let curr_tes = [];
    let curr_caregiver = false;
    for (let record of jdata) {
        let te = new TableElements();
        for (let prop in te) {
            if (record.hasOwnProperty(prop)) {
                if (prop == "child_caregiver_end_date" && record[prop] == null) {
                    curr_caregiver = true;
                }
                te[prop] = record[prop];
            } else {
                te[prop] = null;
            }
        }
        te.href = "child.html?id=" + record.child_id
        if (curr_caregiver) {
            curr_tes.push(te)
            curr_caregiver = false;
        } else {
            hist_tes.push(te);
        }
    }
    return [hist_tes, curr_tes];
}

function constructCarerTable(table_entries, table_id) {
    let headers = [
        "",          // edit link
        "English Name", "Chinese Name",
        "Pinyin Name", "Start Date",
        "End Date", "Note"
    ];
    let columnTypes = [
        columnTypeEnum.editFormLink,
        columnTypeEnum.text, columnTypeEnum.text,
        columnTypeEnum.text, columnTypeEnum.text,
        columnTypeEnum.text, columnTypeEnum.text
    ];
    let fieldNames = [
        "href",
        "caregiver_english_name", "caregiver_chinese_name",
        "caregiver_pinyin_name", "child_caregiver_start_date",
        "child_caregiver_end_date", "child_caregiver_note"
    ];
    let columnData = new ColumnData(headers, columnTypes, fieldNames);
    let tdata = new TableData(table_id, columnData, table_entries);
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
        let hist_tes = tes[0];
        let curr_tes = tes[1];
        // sort g_carer_table_entries by child_caregiver_end_date, most recent to least recent
        hist_tes.sort(function(a, b) {
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
        constructCarerTable(curr_tes, "current_carer_table");
        constructCarerTable(hist_tes, "carer_history_table");
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
