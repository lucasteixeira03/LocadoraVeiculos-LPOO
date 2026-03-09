from .veiculo import Carro, Motorhome, Categoria
from .ExcecoesPersonalizadas import TipoVeiculoInvalidoError

class VeiculoFactory:
    @staticmethod
    def criar_veiculo(tipo, placa, categoria=Categoria.ECONOMICO):
        tipo = tipo.lower().strip()

        if tipo == "carro":
            if categoria == Categoria.ECONOMICO:
                taxa_diaria = 100.0
            else:
                taxa_diaria = 180.0
            return Carro(placa, taxa_diaria, categoria)

        elif tipo == "motorhome":
            if categoria == Categoria.ECONOMICO:
                taxa_diaria = 250.0
            else:
                taxa_diaria = 400.0
            return Motorhome(placa, taxa_diaria, categoria)

        else:
            raise TipoVeiculoInvalidoError("Tipo de veículo inválido! Use 'carro' ou 'motorhome'.")