async function api(url, body, method, res){
    url = "https://devsiproject.vercel.app" + url

    const headers = new Headers({
        "Content-Type": "application/json"
    })

    const payload = {
        method: method,
        headers: headers,
        body: JSON.stringify(body)
    }

    let req = await fetch(url, payload)
        .then(response => response)

    if(req.status == 200) {
        if(res == true){
            let data = await req.json()
            return {"req": req, "data": data}
        }
        return {"req": req}
    }
    
    return new PromiseRejectionEvent("unhandledrejection", {
        promise: req,
        reason: "Failed request."
    })
}

function changeOptions(){
    event.preventDefault()
    route = "/options"

    if(document.getElementById("dias-cancel").value != ""){
        api(route, {"cancel": document.getElementById("dias-cancel").value}, 'POST', false)
            .then(() => {
                document.getElementById("config_sistema").style.display = 'none';
                document.getElementById("dias-cancel").value = "";
                reloadOptions()
            })
    }
    if(document.getElementById("dias-max").value != ""){
        api(route, {"max": document.getElementById("dias-max").value}, 'POST', false)
            .then(() => {
                document.getElementById("config_sistema").style.display = 'none';
                document.getElementById("dias-max").value = "";
                reloadOptions()
            })
    }
    if(document.getElementById("dias-min").value != ""){
        api(route, {"min": document.getElementById("dias-min").value}, 'POST', false)
            .then(() => {
                document.getElementById("config_sistema").style.display = 'none';
                document.getElementById("dias-min").value = "";
                reloadOptions()
            })
    }
}

function reloadOptions(){
    api("/options", {"type": true}, 'POST', true)
        .then(response => {
            document.getElementById("dias-cancel").placeholder = response.data.cancel
            document.getElementById("dias-max").placeholder = response.data.max
            document.getElementById("dias-min").placeholder = response.data.min
        })
}

function getLocalValue(){
    if(document.getElementById("locais").value != ""){
        for(let i=0; i<localInfos.length; i++){
            if(document.getElementById("locais").value == localInfos[i]["nome"]){
                document.getElementById("local-valor").placeholder = localInfos[i]["valor"]
            }
        }
    }
}

function setLocalValue(){
    if(document.getElementById("locais").value != ""){
        console.log("ok")
        document.getElementById("config_alugueis").style.display = 'none';
    }
}