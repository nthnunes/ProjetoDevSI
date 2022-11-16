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

// altera as configurações de sistema
function changeOptions(){
    event.preventDefault()
    route = "/options"

    // verifica quais campos contém algum valor e faz o envio das informações
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

// recarrega as configurações de sistema
function reloadOptions(){
    api("/options", {"type": true}, 'POST', true)
        .then(response => {
            document.getElementById("dias-cancel").placeholder = response.data.cancel
            document.getElementById("dias-max").placeholder = response.data.max
            document.getElementById("dias-min").placeholder = response.data.min
        })
}

// obtém os dados dos locais
function getLocalValue(){
    if(document.getElementById("locais").value != ""){
        for(let i=0; i<localInfos.length; i++){
            if(document.getElementById("locais").value == localInfos[i]["nome"]){
                document.getElementById("local-valor").placeholder = localInfos[i]["valor"]
            }
        }
    }
}

// recarrega os valores dos locais
function reloadLocal(){
    api("/local", {"type": "get"}, 'POST', true)
        .then(response => {
            document.getElementById("local-valor").value = ""
            element = document.getElementById("locais")
            localInfos = response.data.data
            for(let i=0; i<localInfos.length; i++){
                if(document.getElementById("locais").value == localInfos[i]["nome"]){
                    document.getElementById("local-valor").placeholder = localInfos[i]["valor"]
                }
            }
        })
}

// altera o valor de um local
function setLocalValue(){
    if(document.getElementById("locais").value != ""){
        body = {
            "nome": document.getElementById("locais").value,
            "valor": Number(document.getElementById("local-valor").value),
            "type": "edit"
        }

        api("/local", body, 'POST', false)
            .then(() => {
                document.getElementById("config_alugueis").style.display = 'none'
                reloadLocal()
            })
    }
}

// obtém o token dos apartamentos
function getAptoToken(){
    if(document.getElementById("tranfer-user").value != ""){
        for(let i=0; i<aptoInfos.length; i++){
            if(document.getElementById("tranfer-user").value == aptoInfos[i]["apto"]){
                document.getElementById("token-apto").innerText = aptoInfos[i]["token"]
            }
        }
    }
}