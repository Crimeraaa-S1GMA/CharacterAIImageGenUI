function sendGenerateRequest(prompt = "") {
    return fetch("/generate/", {
        method: 'POST',
        mode: 'cors', 
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
        'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({"prompt" : prompt})
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // parses JSON response into native JavaScript objects
    });
}

function generate() {
    let prompt = document.querySelector("#prompt").value;
    if (prompt.length > 0) {
        let status = document.querySelector("#status");
        status.innerHTML = "Generating images...";
        sendGenerateRequest(prompt).then(
            data => {
                showOutputs(data);
            }
        ).catch(
            (error) => {
                console.error(error);
            }
        )
    }
}

function showOutputs(urls) {
    let status = document.querySelector("#status");
    status.innerHTML = "";

    let outputContainer = document.querySelector("#outputs");

    outputContainer.innerHTML = "";
    outputContainer.style.display = "inline-block";

    urls.forEach(element => {
        let image = document.createElement("img");

        image.className = "preview-image";
        image.src = element;

        outputContainer.appendChild(image);
    });
}
