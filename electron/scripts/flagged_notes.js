"use strict";



// THE RESPONSE WAY

//var request = require('request');

//var request = require("request");

//var options = {
//    method: 'GET',
//    url: 'http://127.0.0.1:5000/entity/child_note',
//    qs: { flag: '1' }
//};

//request(options, function (error, response, body) {
//    if (error) throw new Error(error);

//    console.log(body);
//});

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
    }
}


// Function to construct a TableElements object and return it.
function populateTableElements(jdata, note_type, note_name) {
    let tes = [];
    console.log(jdata);
    for (let record of jdata) {
        //console.log(record);
        let te = new TableElements();

        for (let prop in te) {
            te[prop] = record.hasOwnProperty(prop) ? record[prop] : null;
        }
        te.note_type = note_type;
        te.note = record[note_name];
        //console.log(te);
        tes.push(te);
    }
    return tes;
}


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

// global var for table entry data.
let g_table_entries = [];
// TableEntry data is collected - now build the 
function constructTable() {
    console.log(g_table_entries);

}

function initializeTable() {
    const base_url = "http://127.0.0.1:5000";
    const child_note_url = base_url + "/entity/child,child_caregiver,caregiver,child_note?child_note_flag=1";
    const child_assessment_url = base_url + "/entity/child,child_caregiver,caregiver,child_assessment,specialist?child_assessment_note_flag=1"
    const child_partner_url = base_url + "/entity/child,child_caregiver,caregiver,child_partner,partner?child_partner_note_flag=1"
    

    // decrements when each request succeeds so final request can call next step.
    let requests_remaining = 1; // MAKE THIS 3 EVENTUALLY

    makeRequest({
        method: "GET",
        url: child_note_url
    }).then(function (datums) {
        console.log("I got the child_note data!");
        let jdata = JSON.parse(datums);
        let tes = populateTableElements(jdata, "General", "child_note");
        g_table_entries = g_table_entries.concat(tes);
        requests_remaining--;
        if (requests_remaining === 0) {
            constructTable();
        }
    }).catch(function (err) {
        console.error('Error getting child_note data! ', err.statusText);
    });


    //let assessment_flagged_notes = makeRequest(child_assessment_url);
    //let partner_flagged_notes = makeRequest(child_partner_url);


    //tes.concat(populateTableElements(child_flagged_notes, "General", "child_note"));
    //tes.concat(populateTableElements(assessment_flagged_notes, "Assessment", "child_assessment_note"));
    //tes.concat(populateTableElements(partner_flagged_notes, "Partner", "child_partner_note"));

}


// THE JQUERY WAY

//let url = "http://127.0.0.1:5000/entity/child_note?flag=1";
//$.getJSON(url, function (data) {
//    //console.log(data);
//    let headers = ["Child ID", "Date", "Flagged", "Note ID", "Note"];
//    let tbl = document.createElement("TABLE");
//    tbl.setAttribute("id", "note_table");
//    let tbl_header = tbl.createTHead();
//    let header_row = tbl_header.insertRow();
//    for (i = 0; i < headers.length; i++) {
//        let header_cell = header_row.insertCell();
//        header_cell.appendChild(document.createTextNode(headers[i]));
//    }
//    document.body.appendChild(tbl);
//    var tbl_body = document.createElement("tbody");
//    $.each(data, function () {
//        var tbl_row = tbl_body.insertRow();
//        $.each(this, function (k, v) {
//            var cell = tbl_row.insertCell();
//            cell.appendChild(document.createTextNode(v.toString()));
//            console.log(k);
//            console.log(v);
//        })
//    })
//    document.getElementById("note_table").appendChild(tbl_body);
//});