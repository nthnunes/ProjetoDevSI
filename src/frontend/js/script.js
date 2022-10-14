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

    pwd = document.getElementById("senha").value
    regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,25}$/g;
    if(pwd.match(regex) == null) {
        window.alert("A senha deve conter ao menos uma letra minúscula, uma letra maiúscula, um número e um caracter especial, tente novamente!")
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