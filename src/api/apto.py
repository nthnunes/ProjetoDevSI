import random, string

class Apto():
    def __init__(self, descricao, numero, id=None, idUser=None) -> None:
        self.id = id
        self.token = ''.join(random.choice(string.ascii_letters) for i in range(15))
        self.descricao = descricao
        self.idUser = idUser
        self.numero = numero

    def getId(self) -> str:
        return self.id

    def getToken(self) -> str:
        return self.token

    def getDescricao(self) -> str:
        return self.descricao

    def getIdUser(self) -> str:
        return self.idUser

    def getNumero(self) -> int:
        return self.numero