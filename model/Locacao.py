from datetime import date
from .veiculo import Veiculo
from .ExcecoesPersonalizadas import DataInvalidaError

class Locacao:
    def __init__(self, veiculo: Veiculo, data_inicio: date, data_fim: date):
        self.veiculo = veiculo
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    @property
    def veiculo(self):
        return self.__veiculo

    @veiculo.setter
    def veiculo(self, obj):
        if obj is None:
            raise Exception("Objeto Veículo obrigatório!")
        self.__veiculo = obj

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data_inicio):
        if data_inicio is None or not isinstance(data_inicio, date):
            raise DataInvalidaError("Data de início inválida!")
        self.__data_inicio = data_inicio

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data_fim):
        if data_fim is None or not isinstance(data_fim, date):
            raise DataInvalidaError("Data de fim inválida!")
        self.__data_fim = data_fim

    def calcular_valor_locacao(self) -> float:
        if self.data_fim < self.data_inicio:
            raise DataInvalidaError("A data final não pode ser menor que a data inicial.")

        dias = (self.data_fim - self.data_inicio).days + 1

        if dias <= 0:
            raise DataInvalidaError("A locação deve ter pelo menos 1 diária.")

        total = (dias * self.veiculo.taxa_diaria) + self.veiculo.valor_seguro
        return total