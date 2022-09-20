class Reserva():
    def __init__(self, idApto, idLocal, data, valor, status, id=None) -> None:
        self.id = id
        self.idApto = idApto
        self.idLocal = idLocal
        self.data = data
        self.valor = valor
        self.status = status

    def getId(self) -> str:
        return self.id

    def getIdApto(self) -> str:
        return self.idApto

    def getIdLocal(self) -> str:
        return self.idLocal

    def getData(self) -> str:
        return self.data
    
    def getValor(self) -> float:
        return self.valor

    def getStatus(self) -> str:
        return self.status