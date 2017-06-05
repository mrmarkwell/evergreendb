var BASE_URL = "http://127.0.0.1:5000/";


// Enum of legal column types for tableGenerator
let columnTypeEnum = Object.freeze(
    {
        // Standard text data
        text: 0,

        // Link to an edit form for this row. Will become a clickable pencil icon in the table.
        editFormLink: 1,

        // Link to a detailed view for this row. Will become a clickable eyeball icon in the table.
        viewDetailLink: 2,

        // Function to call (without parentheses) when the check box is clicked.
        // Calls the function with params function(this, idx) where 'this' is
        // the checkbox itself (so .checked can be inspected) and idx is the index of the row object being created. 
        checkboxFunc: 3
    })

// ColumnData Class. Specifies details about the columns to be constructed by tableGenerator.
function ColumnData(headerList, columnTypeList, fieldNameList) {
    return {
        // List of string text to be displayed to the user as the header of this column.
        // Use an empty string to create a blank header column.
        headerText: headerList,

        // List of columnTypeEnums of the columns. See columnTypeEnum for details.
        columnType: columnTypeList,

        // List of names of the fields to be extracted from the data object for this column.
        fieldName: fieldNameList
    }
}

// TableData Class. An instance of this class is passed to tableGenerator() to construct a table.
function TableData(id, columns, objects, checkedDecision) {
    return {
        // ID of the table in the HTML. 
        // Table should be defined in HTML but have no elements within.
        // generateTable will populate all table elements.
        tableID: id,

        // ColumnData object that defines the columns of this table.
        columnData: columns,

        // List of custom objects that contain all the data needed to
        // construct a row of the table. One object per row.
        // Fields in these objects should have names matching the "fieldName" 
        // element of the ColumnData objects.
        tableElementObjects: objects,

        // if a checkbox is included, this function should return true if the box should
        // be checked on window load, false otherwise
        checkedDecisionFunc: checkedDecision
    }
}

// Generate a table with a TableData object.
function generateTable(tdata) {
    // Get the table.
    let table = document.getElementById(tdata.tableID);

    // Add a table header and populate it with the column headers
    let thead = document.createElement("thead");
    let tr = document.createElement("tr");
    for (let headerText of tdata.columnData.headerText) {
        let td = document.createElement("td");
        let headerTextNode = document.createTextNode(headerText);
        td.appendChild(headerTextNode);
        tr.appendChild(td);
    }
    thead.appendChild(tr);
    table.appendChild(thead);

    // Add the table body and populate all the rows
    let tbody = document.createElement("tbody");
    for (let [rowIdx, obj] of tdata.tableElementObjects.entries()) {
        // Construct the row based on the type it is
        let fields = tdata.columnData.fieldName;
        let tr = document.createElement("tr");
        for (let [colIdx, type] of tdata.columnData.columnType.entries()) {
            let field = fields[colIdx];
            let cellData = obj[field];
            let td = document.createElement("td");
            if (type == columnTypeEnum.text) {
                let textNode = document.createTextNode(cellData);
                td.appendChild(textNode);
                // implement text option
            } else if (type == columnTypeEnum.editFormLink || type == columnTypeEnum.viewDetailLink) {
                let imgLink = type == columnTypeEnum.editFormLink ? "./css/images/pencil.png" : "./css/images/view.png";
                let a = document.createElement("a");
                a.href = cellData;
                a.title = "Edit Row";
                let img = document.createElement("img");
                img.border = 0;
                img.alt = "edit";
                img.src = imgLink;
                img.width = 24;
                img.height = 24;
                a.appendChild(img);
                td.appendChild(a);
            } else if (type == columnTypeEnum.checkboxFunc) {
                let input = document.createElement("input");
                input.type = "checkbox";
                input.setAttribute("onchange", "" + cellData + "(this, " + rowIdx + ", " + JSON.stringify(obj).replace(/"/g, "'") + ")");
                if (typeof tdata.checkedDecisionFunc != 'undefined') {
                    input.checked = tdata.checkedDecisionFunc(obj)
                }
                td.appendChild(input);
            } else {
                console.error("Unknown column type in generateTable: " + type);
            }
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
}


// Get the query parameters of the current page (not visable in electron)
function getParameterByName(name, url) {
    var regex = new RegExp("[?&]" + name + "=([^&#]*)(&|$|#)");
    if (!url) url = window.location.href;
    results = regex.exec(url);
    if (!results) return null;
    if (!results[1]) return '';
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Run a REST GET with callback
function restGet(relative_url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status >= 300) {
                badRequest(this.status, JSON.parse(this.responseText));
            } else {
                callback(JSON.parse(this.responseText));
            }
        }
    });
    xhr.open("GET", BASE_URL + relative_url);
    xhr.setRequestHeader("cache-control", "no-cache");
    xhr.send(null);
}

function restPost(relative_url, body, callback) {
    let data = JSON.stringify(body);

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status >= 300) {
                badRequest(this.status, JSON.parse(this.responseText));
            } else {
                callback(JSON.parse(this.responseText));
            }
        }
    });

    xhr.open("POST", BASE_URL + relative_url);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("accept", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(data);
}

function restDelete(relative_url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status >= 300) {
                badRequest(this.status, JSON.parse(this.responseText));
            } else {
                callback();
            }
        }
    });

    xhr.open("DELETE", BASE_URL + relative_url);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("accept", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(null);
}

function restPut(relative_url, body, callback) {
    let data = JSON.stringify(body);

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status >= 300) {
                badRequest(this.status, JSON.parse(this.responseText));
            } else {
                callback(JSON.parse(this.responseText));
            }
        }
    });

    xhr.open("PUT", BASE_URL + relative_url);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("accept", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(data);
}

function badRequest(ret_status, json) {
    let error_str = "";
    for (let i in json.message) {
        error_str += "Error " + ret_status + " with " + i + ":\n  " + json.message[i] + "\n";
    }
    console.log(error_str);
    window.alert(error_str);
}

// Function to handle asynchronous HTTP requests with promises.
/* Takes opts:
{
  method: String,
  url: String,
  params: String | Object,
  headers: Object,
  responseType: String
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
        
        //if request is not using auth try and add it from cached auth created from login
        if (!opts.headers) {
            opts.headers = {};
        }
        if (!opts.headers.hasOwnProperty('Authorization')) {
            var username = sessionStorage.getItem("username");
            var password = sessionStorage.getItem("password");
            if (sessionStorage.getItem("username") != null) {
                opts.headers.Authorization = "Basic " + btoa(username + ":" + password);
            }
        }
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
