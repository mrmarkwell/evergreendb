let url = getBaseURL() + "entity/child";

function getAllChildren(callback) {
  var xhr = new XMLHttpRequest();
  xhr.withCredentials = true;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
      callback(JSON.parse(this.responseText));
    }
  });
  xhr.open("GET", url);
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
    table += "<tr id="+json[i].id+" onclick=\"loadChild(id)\">";
    for (var j=0; j<columns.length; j++) {
      table += "<td>" + json[i][columns[j]];
    }
  }

  // write to table
  table_ref.innerHTML = table;
}

function loadChild(child_id) {
	window.document.location="child.html?id="+child_id;
}

getAllChildren(function (json) {
    jsonTable(json, document.getElementById("child_table"), ["child_english_name", "birth_date"]);
});