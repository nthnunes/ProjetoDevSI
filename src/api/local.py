class Local():
    def __init__(self, nome, valor, id=None) -> None:
        self.id = id
        self.nome = nome
        self.valor = valor

    def getId(self) -> str:
        return self.id

    def getNome(self) -> str:
        return self.nome

    def getValor(self) -> float:
        return self.valor