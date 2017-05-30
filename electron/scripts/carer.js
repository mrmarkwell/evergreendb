const settings = require('electron-settings');

// global var for table entry data
let g_table_entries = [];

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
    d_log(jdata)
    let tes = [];
    for (let record of jdata) {
        d_log(record)
        let te = new TableElements();
        for (let prop in te) {
            te[prop] = record.hasOwnProperty(prop) ? record[prop] : null;
        }
        d_log(te)
        tes.push(te);
    }
    return tes;
}

function constructTable() {
    // d_log(g_table_entries);
    let headers = [
        "caregiver_english_name", "caregiver_chinese_name",
        "caregiver_pinyin_name", "child_caregiver_start_date",
        "child_caregiver_end_date", "child_caregiver_note"
    ]
    let tbody = document.getElementById("carer_table_body")
    for (let entry of g_table_entries) {
        let tr = document.createElement("tr");
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
    const base_url = "http://127.0.0.1:5000";
    const caregiver_url = base_url + "/entity/child,child_caregiver,caregiver?child_id=" + child_id
    d_log(caregiver_url)

    // decrements when each request succeeds so final request can call next step.
    let requests_remaining = 1;
    let table_names = ["carer_data"];
    let urls = [caregiver_url];


    for (let i = 0; i < table_names.length; i++) {
        makeRequest({
            method: "GET",
            url: urls[i]
        }).then(function (datums) {
            d_log("I got the data!");
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

function submitNewCaregiver() {
    pass
}
