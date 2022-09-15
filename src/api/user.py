class User():
    def __init__(self, email, senha, nome, telefone, permissao, id=None) -> None:
        self.id = id
        self.email = email
        self.senha = senha
        self.nome = nome
        self.telefone = telefone
        self.permissao = permissao

    def getId(self) -> str:
        return self.id

    def getEmail(self) -> str:
        return self.email

    def getSenha(self) -> str:
        return self.senha

    def getTelefone(self) -> str:
        return self.telefone

    def getPermissao(self) -> bool:
        return self.permissao