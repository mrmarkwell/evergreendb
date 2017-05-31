const settings = require('electron-settings');

// global var for table entry data
let g_table_entries = [];
const g_base_url = "http://127.0.0.1:5000";

// log to console if in debug mode
function d_log(record) {
    let in_debug_mode = settings.get('debug')
    if (in_debug_mode) {
        console.log(record);
    }
}

// Function to handle asynchronous HTTP requests with promises.
/* Takes opts:
{
  method: String,
  url: String,
  params: String | Object,
  headers: Object
}
*/
function makeRequest(opts) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open(opts.method, opts.url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        if (opts.headers) {
            Object.keys(opts.headers).forEach(function (key) {
                xhr.setRequestHeader(key, opts.headers[key]);
            });
        }
        if (opts.responseType) {
            xhr.responseType = opts.responseType;
        }
        var params = opts.params;
        // We'll need to stringify if we've been given an object
        // If we have a string, this is skipped.
        if (params && typeof params === 'object') {
            params = Object.keys(params).map(function (key) {
                return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
            }).join('&');
        }
        xhr.send(params);
    });
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
function populateTableElements(jdata) {
    let tes = [];
    for (let record of jdata) {
        let te = new TableElements();
        for (let prop in te) {
            te[prop] = record.hasOwnProperty(prop) ? record[prop] : null;
        }
        tes.push(te);
    }
    return tes;
}

function constructTable() {
    let headers = [
        "caregiver_english_name", "caregiver_chinese_name",
        "caregiver_pinyin_name", "child_caregiver_start_date",
        "child_caregiver_end_date", "child_caregiver_note"
    ]
    let tbody = document.getElementById("carer_table_body")
    for (let entry of g_table_entries) {
        let tr = document.createElement("tr");
        if (!entry["child_caregiver_end_date"]) {   // current caregiver
            tr.classList.add("highlight")
            entry["child_caregiver_end_date"] = "Current"
        }
        for (let header of headers) {
            let td = document.createElement("td");
            td.appendChild(document.createTextNode(entry[header]));
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
}

// Main entry point. Do all the initial REST calls and get all the data.
// Construct the table.
function initializeCarerTable(child_id) {
    const caregiver_url = g_base_url + "/entity/child,child_caregiver,caregiver?child_id=" + child_id

    // decrements when each request succeeds so final request can call next step.
    let requests_remaining = 1;
    let table_names = ["carer_data"];
    let urls = [caregiver_url];


    for (let i = 0; i < table_names.length; i++) {
        makeRequest({
            method: "GET",
            url: urls[i]
        }).then(function (datums) {
            let jdata = JSON.parse(datums);
            let tes = populateTableElements(jdata);
            g_table_entries = g_table_entries.concat(tes);
            requests_remaining--;
            if (requests_remaining === 0) {
                // sort g_table_entries by child_caregiver_end_date, most recent to least recent
                g_table_entries.sort(function(a, b) {
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
                constructTable();
            }
        }).catch(function (err) {
            console.error('Error getting data from ' + table_names[i], err.statusText);
        });
    }
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
