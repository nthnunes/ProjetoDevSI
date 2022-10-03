async function api(url, body, method){
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
    let data = await req.json()

    return {"req": req, "data": data}
}

function login(){
    event.preventDefault()
    route = "/login"

    let email = document.getElementById("email").value
    let senha = document.getElementById("senha").value

    body = {
        "email": email,
        "senha": senha
    }

    api(route, body, 'POST')
        .then(response => {
            localStorage.setItem("id", response.data.id)
            console.log(response.req.status)
        })
}