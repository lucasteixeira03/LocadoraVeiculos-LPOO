from datetime import date
from model.veiculo import Categoria
from model.veiculo_factory import VeiculoFactory
from model.Locacao import Locacao


print("=== TESTE 1: Criação via Factory ===")
try:
    veiculo1 = VeiculoFactory.criar_veiculo("carro", "ABC1234", Categoria.ECONOMICO)
    print("Veículo criado com sucesso:", type(veiculo1).__name__, veiculo1.placa, veiculo1.taxa_diaria)
except Exception as e:
    print("Erro:", e)


print("\n=== TESTE 2: Cálculo com múltiplos dias ===")
try:
    veiculo2 = VeiculoFactory.criar_veiculo("carro", "DEF1G34", Categoria.EXECUTIVO)
    locacao1 = Locacao(
        veiculo=veiculo2,
        data_inicio=date(2025, 6, 1),
        data_fim=date(2025, 6, 3)
    )
    print("Valor total da locação:", locacao1.calcular_valor_locacao())
except Exception as e:
    print("Erro:", e)


print("\n=== TESTE 3: Devolução no mesmo dia ===")
try:
    veiculo3 = VeiculoFactory.criar_veiculo("motorhome", "XYZ9999", Categoria.ECONOMICO)
    locacao2 = Locacao(
        veiculo=veiculo3,
        data_inicio=date(2025, 6, 10),
        data_fim=date(2025, 6, 10)
    )
    print("Valor total da locação:", locacao2.calcular_valor_locacao())
except Exception as e:
    print("Erro:", e)


print("\n=== TESTE 4: Tipo inválido na fábrica ===")
try:
    veiculo4 = VeiculoFactory.criar_veiculo("moto", "AAA1234", Categoria.ECONOMICO)
except Exception as e:
    print("Erro:", e)


print("\n=== TESTE 5: Datas inválidas ===")
try:
    veiculo5 = VeiculoFactory.criar_veiculo("carro", "BBB1234", Categoria.ECONOMICO)
    locacao3 = Locacao(
        veiculo=veiculo5,
        data_inicio=date(2025, 6, 5),
        data_fim=date(2025, 6, 2)
    )
    print("Valor total da locação:", locacao3.calcular_valor_locacao())
except Exception as e:
    print("Erro:", e)