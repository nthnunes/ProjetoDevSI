import random, string

class Apto():
    def __init__(self, descricao, numero, id=None, idApto=None) -> None:
        self.id = id
        self.token = ''.join(random.choice(string.ascii_letters) for i in range(15))
        self.descricao = descricao
        self.idApto = idApto
        self.numero = numero

    def getId(self) -> str:
        return self.id

    def getToken(self) -> str:
        return self.token

    def getDescricao(self) -> str:
        return self.descricao

    def getIdApto(self) -> str:
        return self.idApto

    def getNumero(self) -> int:
        return self.numero