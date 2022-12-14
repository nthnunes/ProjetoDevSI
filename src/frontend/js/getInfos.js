async function recent(url, body){
    url = "https://devsiproject.vercel.app" + url

    const payload = {
        method: 'POST',
        headers: new Headers({"Content-Type": "application/json"}),
        body: JSON.stringify(body)
    }

    let req = await fetch(url, payload)
        .then(response => response)

    if(req.status == 200) {
        let data = await req.json()
        return {"req": req, "data": data}
    }
    
    return new PromiseRejectionEvent("unhandledrejection", {
        promise: req,
        reason: "Failed request."
    })
}

// preenche as informações sobre os aluguéis recentes
recent("/recent", {"id": window.localStorage.getItem('id')})
    .then(response => {
        if(response.req.status == 200){
            element = document.getElementById("recent")
            data = response.data.data
            // se for um usuário comum preenche com os aluguéis linkados com seu id
            if(response.data.permissao == false){
                if(data.length == 0){
                    element.innerHTML = "<p>Você não possui alugueis.</p>"
                }
                for(let i=0; i<data.length; i++){
                    element.innerHTML = element.innerHTML + "<div class=\"agendamentos\" ><div>" + data[i]["local"] + "</div><div>" + data[i]["data"] + "</div><div>" + data[i]["valor"].toLocaleString('pt-br',{style: 'currency', currency: 'BRL'}) + "</div></div>"
                }
            }
            // caso seja usuário admin preenche com as informações de todos usuários
            else{
                if(data.length == 0){
                    element.innerHTML = "<p>Não há alugueis em aberto.</p>"
                }
                for(let i=0; i<data.length; i++){
                    element.innerHTML = element.innerHTML + "<div class=\"agendamentos\" ><div>" + data[i]["nome"] + "</div><div>" + data[i]["data"] + "</div><div>" + data[i]["local"].toLocaleString('pt-br',{style: 'currency', currency: 'BRL'}) + "</div></div>"
                }
            }
        }
    })

// preenche as informações sobre configurações de sistema
recent("/options", {"type": true})
    .then(response => {
        document.getElementById("dias-cancel").placeholder = response.data.cancel
        document.getElementById("dias-max").placeholder = response.data.max
        document.getElementById("dias-min").placeholder = response.data.min
    })

// preenche todos os locais salvos
recent("/local", {"type": "get"})
    .then(response => {
        element = document.getElementById("locais")
        localInfos = response.data.data
        for(let i=0; i<localInfos.length; i++){
            element.innerHTML = element.innerHTML + "<option value=\"" + localInfos[i]["nome"] + "\">" + localInfos[i]["nome"] + "</option>"
        }
    })

// preenche todos os apartamentos salvos
recent("/transfer", {"type": true})
    .then(response => {
        element = document.getElementById("tranfer-user")
        aptoInfos = response.data.data
        for(let i=0; i<aptoInfos.length; i++){
            element.innerHTML = element.innerHTML + "<option value=\"" + aptoInfos[i]["apto"] + "\">" + aptoInfos[i]["apto"] + "</option>"
        }
    })