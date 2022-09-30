async function api(url, body){
    url = "https://devsiproject.vercel.app" + url

    const headers = new Headers({
        "Content-Type": "application/json"
    })

    const payload = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    }

    let req = await fetch(url, payload)
        .then(response => response.json())
    localStorage.setItem("id", req.id)

    return req.permissao
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

    api(route, body)
        .then(response => console.log(response))
}