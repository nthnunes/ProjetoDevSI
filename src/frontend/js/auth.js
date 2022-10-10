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
            console.log(JSON.stringify(response.data))
        }
    })
    .catch(response => {
        localStorage.clear()
        window.location.replace("https://nthnunes.github.io/ProjetoDevSI/src/frontend/pages/forbidden.html")
        setTimeout(10000)
        window.location.replace("https://nthnunes.github.io/ProjetoDevSI/")
    })