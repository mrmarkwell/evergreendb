function getAllChildren(callback) {
  var xhr = new XMLHttpRequest();
  xhr.withCredentials = true;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
      console.log(this.responseText);
      callback(JSON.parse(this.responseText));
    }
  });
  xhr.open("GET", "http://127.0.0.1:5000/entity/child");
  xhr.send(null);
}

function jsonTable(json, table_ref, columns) {
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
  table_ref.innerHTML = table;
}
