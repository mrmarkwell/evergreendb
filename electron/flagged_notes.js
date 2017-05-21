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

// THE XMLHttpRequest WAY

//var note_data = null;

//var xhr = new XMLHttpRequest();
//xhr.withCredentials = true;

//xhr.addEventListener("readystatechange", function () {
//    if (this.readyState === 4) {
//        //console.log(this.responseText);
//    }
//});

//xhr.open("GET", "http://127.0.0.1:5000/entity/child_note?flag=1");

//xhr.send(note_data);

//let flagged_notes = JSON.parse(data);

// THE JQUERY WAY

let url = "http://127.0.0.1:5000/entity/child_note?flag=1";
$.getJSON(url, function (data) {
    //console.log(data);
    let headers = ["Child ID", "Date", "Flagged", "Note ID", "Note"];
    let tbl = document.createElement("TABLE");
    tbl.setAttribute("id", "note_table");
    let tbl_header = tbl.createTHead();
    let header_row = tbl_header.insertRow();
    for (i = 0; i < headers.length; i++) {
        let header_cell = header_row.insertCell();
        header_cell.appendChild(document.createTextNode(headers[i]));
    }
    document.body.appendChild(tbl);
    var tbl_body = document.createElement("tbody");
    $.each(data, function () {
        var tbl_row = tbl_body.insertRow();
        $.each(this, function (k, v) {
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v.toString()));
            console.log(k);
            console.log(v);
        })
    })
    document.getElementById("note_table").appendChild(tbl_body);
});