//TODO Change 127.0.0.1 to static ip of web server

var reaction = "none"


function getUrlParameter(name) {
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    var results = regex.exec(window.location.href);
    if (!results) {
        return null;
    }
    if (!results[2]) {
        return '';
    }
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}








function generateToken() {
    var characters = '0123456789';
    var token = '';

    for (let i = 0; i < 13; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        token += characters[randomIndex];
    }

    return token;
}


function save_state() {
    var elem = document.getElementById("editor");
    var top = document.getElementById("topic");

    if (getUrlParameter('id') == null) {
        //we are not editing state

        const tok = generateToken();
        console.log(tok);

        fetch("http://127.0.0.1:8000/new_state/", {
                method: "POST",
                body: JSON.stringify({
                    token: tok,
                    state_data: elem.innerHTML,
                    topic: top.innerHTML,
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                console.log(tok);
                window.location.replace("http://127.0.0.1:8000/state/?id=" + tok);
            });
    } else {
        //we are editing state
        var tok = getUrlParameter("id");
        console.log(tok);





        fetch("http://127.0.0.1:8000/new_state/", {
                method: "POST",
                body: JSON.stringify({
                    token: tok,
                    state_data: elem.innerHTML,
                    topic: top.innerHTML,
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                console.log(tok);
                window.location.replace("http://127.0.0.1:8000/state/?id=" + tok);
            });
    }
}





function insert_photo() {
    var elem = document.getElementById("editor");
    var input = document.createElement("input");
    input.setAttribute("id", "file_upd");
    input.setAttribute("accept", "image/png, image/gif, image/jpeg");
    input.type = "file";
    input.click();
    input.onchange = function() {
        var photo = input.files[0];
        var formData = new FormData();
        formData.append("photo", photo);
        fetch("http://127.0.0.1:8000/upload_image/", { method: "POST", body: formData })
            .then(response => {
                if (response.ok) {
                    elem.innerHTML += `<img src="http://127.0.0.1:8000/media/images/${photo.name}" style="width:100vh;height:100vh;">`;
                }
            });

    }
}


async function edit_state_data() {
    const id = getUrlParameter('id');
    console.log(id);

    if (id != null) {

        const topic = document.getElementById("topic");
        const text = document.getElementById("editor");

        const response = await fetch("http://127.0.0.1:8000/api/state/", {
            method: "POST",
            body: JSON.stringify({
                tok: id,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })

        if (response.ok) {
            console.log('editing the page');
            var json = await response.json();
            console.log(json);
            topic.innerHTML = json[0];
            text.innerHTML = json[1];
        }
    }
}