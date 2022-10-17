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

function login(){
    event.preventDefault()
    route = "/login"

    body = {
        "email": document.getElementById("email").value,
        "senha": document.getElementById("senha").value
    }

    api(route, body, 'POST', true)
        .then(response => {
            if(response.req.status == 200){
                localStorage.setItem("id", response.data.id)
                if(response.data.permissao == true){
                    window.location.replace("https://nthnunes.github.io/ProjetoDevSI/src/frontend/pages/dashboard.html")
                }
                else{
                    localStorage.setItem("nome", response.data.nome)
                }
            }
        })
        .catch(response => window.alert("Login incorreto, verifique seu email e senha."))
}

function register(){
    event.preventDefault()
    route = "/register"

    email = document.getElementById("email").value
    regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    if(email.match(regex) == null){
        window.alert("Insira um email válido.")
        return false
    }

    pwd = document.getElementById("senha").value
    regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,25}$/g;
    if(pwd.match(regex) == null) {
        window.alert("A senha deve conter ao menos 8 caracteres, uma letra minúscula, uma letra maiúscula, um número e um caracter especial, tente novamente!")
        return false
    }

    body = {
        "token": document.getElementById("token").value,
        "nome": document.getElementById("nome").value,
        "telefone": document.getElementById("telefone").value,
        "email": document.getElementById("email").value,
        "senha": document.getElementById("senha").value
    }

    api(route, body, 'POST', false)
        .then(response => {
            if(response.req.status == 200){
                window.alert("Cadastro concluído, efetue o login para prosseguir.")
                window.location = "https://nthnunes.github.io/ProjetoDevSI/";
            }
        })
        .catch(response => window.alert("Ocorreu um erro, verifique o token."))
}

function forgetPassword(){
    event.preventDefault()
    route = "/resetpassword"

    email = document.getElementById("email").value
    regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    if(email.match(regex) == null){
        window.alert("Insira um email válido.")
        return false
    }

    body = {
        "email": document.getElementById("email").value
    }

    api(route, body, 'POST', false)
        .then(response => {
            window.alert("Se os dados estiverem corretos você receberá um email contendo um token para redifinir sua senha.")
            window.location = "https://nthnunes.github.io/ProjetoDevSI/"
        })
}

function resetPassword(){
    event.preventDefault()
    route = "/resetpassword"

    if(document.getElementById("senha").value != document.getElementById("confirm").value){
        window.alert("As senhas não coincidem, tente novamente!")
        return false
    }

    pwd = document.getElementById("senha").value
    regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,25}$/g;
    if(pwd.match(regex) == null) {
        window.alert("A senha deve conter ao menos 8 caracteres, uma letra minúscula, uma letra maiúscula, um número e um caracter especial, tente novamente!")
        return false
    }

    body = {
        "token": document.getElementById("token").value,
        "senha": document.getElementById("senha").value
    }

    api(route, body, 'POST', false)
        .then(response => {
            if(response.req.status == 200){
                window.alert("Sua senha foi alterada com sucesso.")
                window.location.replace("https://nthnunes.github.io/ProjetoDevSI/")
            }
        })
        .catch(response => window.alert("Token inválido!"))
}