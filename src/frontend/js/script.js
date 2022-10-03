import api from './api.js'

function login(){
    event.preventDefault()
    route = "/login"

    body = {
        "email": document.getElementById("email").value,
        "senha": document.getElementById("senha").value
    }

    api(route, body, 'POST', true)
        .then(response => {
            localStorage.setItem("id", response.data.id)
            console.log(response.req.status)
        })
        .catch(response => console.log('Login failed.'))
}

function register(){
    event.preventDefault()
    route = "/register"

    body = {
        "token": document.getElementById("token").value,
        "nome": document.getElementById("nome").value,
        "telefone": document.getElementById("telefone").value,
        "email": document.getElementById("email").value,
        "senha": document.getElementById("senha").value
    }

    api(route, body, 'POST', false)
        .then(response => console.log(response))
}