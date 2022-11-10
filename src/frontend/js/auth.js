async function api(id){
    url = "https://devsiproject.vercel.app/infos"

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
            if(response.data.permissao == false){
                const welcome = document.getElementById("bem-vindo")
                welcome.innerText = window.localStorage.getItem("nome")
            }
            else{
                document.getElementById("cancel").innerText = response.data.cancelamentos
                document.getElementById("ganhos").innerText = response.data.ganhos.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'})
                document.getElementById("locados-mes").innerText = response.data.locados
                document.getElementById("locados-ano").innerText = response.data.locadosAno
                document.getElementById("reservas").innerText = response.data.reservas
            }
        }
    })
    .catch(response => {
        localStorage.clear()
        window.location.replace("https://nthnunes.github.io/ProjetoDevSI/src/frontend/pages/forbidden.html")
    })