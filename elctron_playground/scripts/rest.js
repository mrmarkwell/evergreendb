function restRun(method,url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", url, false ); // false for synchronous request
  xmlHttp.send( null );
  return xmlHttp.responseText;
}

function restGet(url) {
  return JSON.parse(restRun("GET", url));
}
