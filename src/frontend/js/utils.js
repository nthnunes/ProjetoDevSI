async function api(body){
    url = "https://devsiproject.vercel.app/password"

    const payload = {
        method: 'POST',
        headers: new Headers({"Content-Type": "application/json"}),
        body: JSON.stringify(body)
    }

    let req = await fetch(url, payload)
        .then(response => response)

    return req
}

function changePassword(){
    event.preventDefault()

    if(document.getElementById("newpassword").value != document.getElementById("confirm").value){
        window.alert("As senhas não coincidem, tente novamente.")
        return false
    }

    pwd = document.getElementById("newpassword").value
    regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,25}$/g;
    if(pwd.match(regex) == null) {
        window.alert("A senha deve conter ao menos 8 caracteres, uma letra minúscula, uma letra maiúscula, um número e um caracter especial.")
        return false
    }

    body = {
        "id": window.localStorage.getItem('id'),
        "password": document.getElementById("password").value,
        "newpassword": document.getElementById("newpassword").value
    }

    api(body)
        .then(response => {
            if(response.status == 200){
                window.alert("Senha alterada com sucesso.")
                document.getElementById("editar_senha").style.display = 'none';
                document.getElementById("password").value = "";
                document.getElementById("newpassword").value = "";
                document.getElementById("confirm").value = "";
            }
            else{
                window.alert("A senha atual está incorreta.")
            }
        })
}

function exit(){
    if(confirm("Tem certeza que deseja sair?")){
        localStorage.clear()
        window.location.replace("https://nthnunes.github.io/ProjetoDevSI/")
    }
}