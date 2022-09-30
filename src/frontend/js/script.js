function api(url, body){
    url = "https://devsiproject.vercel.app" + url

    let request = new XMLHttpRequest()
    request.open("GET", url, true)
    request.setRequestHeader("Content-type", "application/json")

    request.onload = () => {
        console.log(this.responseText)
        console.log(this.status)
    }
    request.send(body)
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
}