function restRun(method,url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( method, url, false ); // false for synchronous request
  xmlHttp.send( null );
  return xmlHttp.responseText;
}

function restGet(url) {
  return JSON.parse(restRun("GET", url));
}

function restPost(url,data) { // Create

}

function restPut(url,data) { // Update

}

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
