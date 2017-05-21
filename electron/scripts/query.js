function getAllChildren(callback) {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = true;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
      console.log(this.responseText);
      callback(JSON.parse(this.responseText),"child_table",["english_name"]);
    }
  });
  xhr.open("GET", "http://127.0.0.1:5000/entity/child");
  xhr.setRequestHeader("cache-control", "no-cache");
  xhr.setRequestHeader("postman-token", "a34d63fa-7642-c59d-b236-8437ff0d2068");
  xhr.send(data);
}

function jsonTable(table_id, json, columns) {
  // header row
  var table = "<tr>";
  for (var i=0; i<columns.length; i++) {
    table += "<th>" + columns[i] + "</th>";
  }
  table += "</tr>";

  // data rows
  for (var i=0; i<json.length; i++) {
    table += "<tr>";
    for (var j=0; j<columns.length; j++) {
      table += "<td>" + json[i][columns[j]];
    }
  }

  // write to table
  document.getElementById(table_id).innerHTML = table;
}
