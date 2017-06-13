const g_base_url = getBaseURL();

function findUserByName(datums, username) {
    return datums.find(function(obj) {
        return obj.username === username;
    });
}


function validate(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var user;
    makeRequest({
        method: "GET",
        url: g_base_url + "user",
        headers: {"Authorization": "Basic " + btoa(username + ":" + password)},
        responseType: "json"
    }).then(function(datums) {
        // TODO: Need to check that this an array first...
        if (datums.length == 1) {
            user = datums[0];
        }
        else {
            user = findUserByName(datums, username)
        }
        alert(`Logged in as user id ${user.id} user name: ${user.username} admin: ${user.is_admin} editor: ${user.is_editor}`)
        //TODO: remove password from session storage
        sessionStorage.setItem("username", username);
        sessionStorage.setItem("password", password);
        window.location = "index.html";
    }).catch(function (err) {
        if (err.status == 401) {
            alert("Incorrect username or password, please try again")
            document.getElementById("password").value = "";
        }
        else {
            console.error('Error logging in ' + err.statusText);
        }
    });
}