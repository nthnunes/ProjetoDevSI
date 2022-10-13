function exit(){
    if(confirm("Tem certeza que deseja sair?")){
        localStorage.clear()
        window.location.replace("https://nthnunes.github.io/ProjetoDevSI/")
    }
}