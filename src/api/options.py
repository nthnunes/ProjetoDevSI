class Options():
    def __init__(self, diasCancel, diasMax, diasMin) -> None:
        self.id = "631a7e6387f49dacbfb5efd8"
        self.diasCancel = diasCancel
        self.diasMax = diasMax
        self.diasMin = diasMin

    def getDiasCancel(self) -> int:
        return self.diasCancel

    def getDiasMax(self) -> int:
        return self.diasMax

    def getDiasMin(self) -> int:
        return self.diasMin

    def setDiasCancel(self, dias) -> None:
        self.diasCancel = dias

    def setDiasMax(self, dias) -> None:
        self.diasMax = dias

    def setDiasMin(self, dias) -> None:
        self.diasMin = dias