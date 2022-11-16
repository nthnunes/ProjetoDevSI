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

// verifica se o id salvo é válido
api(window.localStorage.getItem('id'))
    .then(response => {
        if(response.req.status == 200){
            // se o id pertença a um usuário comum altera o texto com o nome salvo
            if(response.data.permissao == false){
                const welcome = document.getElementById("bem-vindo")
                welcome.innerText = window.localStorage.getItem("nome")
            }
            // caso o id seja de um usuário administrador preenche os dados das estatística
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