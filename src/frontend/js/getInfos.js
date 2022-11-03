async function api(id){
    url = "https://devsiproject.vercel.app/recent"

    const payload = {
        method: 'POST',
        headers: new Headers({"Content-Type": "application/json"}),
        body: JSON.stringify({"id": id})
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

api(window.localStorage.getItem('id'))
    .then(response => {
        if(response.req.status == 200){
            element = document.getElementById("recent")
            data = response.data.data
            if(response.data.permissao == false){
                if(data.length == 0){
                    element.innerHTML = "<p>Você não possui alugueis.</p>"
                }
                for(let i=0; i<data.length; i++){
                    element.innerHTML = element.innerHTML + "<div class=\"agendamentos\" ><div>" + data[i]["local"] + "</div><div>" + data[i]["data"] + "</div><div>" + data[i]["valor"].toLocaleString('pt-br',{style: 'currency', currency: 'BRL'}) + "</div></div>"
                }
            }
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