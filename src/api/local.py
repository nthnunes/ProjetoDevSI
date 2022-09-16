class Local():
    def __init__(self, nome, valor, id=None) -> None:
        self.id = id
        self.nome = nome
        self.valor = valor
        self.alugueis = []

    def getId(self) -> str:
        return self.id

    def getNome(self) -> str:
        return self.nome

    def getValor(self) -> float:
        return self.valor

    def addReserva(self, id) -> None:
        self.alugueis.append(id)

    def getReservas(self) -> list:
        return self.alugueis