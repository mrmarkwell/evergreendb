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
        href: null
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
        //console.log(te);
        tes.push(te);
    }
    return tes;
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


// TableEntry data is collected - now build the table itself.
function constructTable() {
    console.log(g_table_entries);
    let headers = ["note_type", "child_english_name", "caregiver_english_name", "note"];
    let tbody = document.getElementById("flagged_notes_table_body");
    for (let entry of g_table_entries) {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        let a = document.createElement("a");
        let link_text = document.createTextNode("Go To Note");
        a.appendChild(link_text);
        a.title = "Go To Note";
        a.href = entry.href;
        td.appendChild(a);
        tr.appendChild(td);
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
        console.error("Error setting up child select dropdown!", err.statusText);
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
        console.error("Error setting up caregiver select dropdown!", err.statusText);
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
            console.error('Error getting data from ' + table_names[i], err.statusText);
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

