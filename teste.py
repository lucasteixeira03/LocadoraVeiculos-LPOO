from datetime import date
from model.locacao import Locacao
from model.veiculo import VeiculoFactory, Categoria
from model.decoradores import GPSDecorator, SeguroTerceirosDecorator

print("\n--- TESTANDO O PADRÃO STATE RESTRITIVO ---")

carro_estado = VeiculoFactory.criar_veiculo(
    "carro",
    "HJI3K45",
    Categoria.ECONOMICO,
    taxa_diaria=100.0
)

# 1. Tentar alugar um carro disponível
carro_estado.tentar_alugar()

# 2. Tentar alugar novamente
carro_estado.tentar_alugar()

# 3. Tentar mandar para manutenção enquanto está alugado
carro_estado.reter_na_frota_pra_conserto()

# 4. Devolver o veículo
carro_estado.tentar_devolver()

# 5. Enviar para manutenção
carro_estado.reter_na_frota_pra_conserto()

# 6. Tentar alugar enquanto está em manutenção
carro_estado.tentar_alugar()

# 7. Finalizar manutenção / devolver ao pátio
carro_estado.tentar_devolver()

# 8. Alugar novamente após voltar a ficar disponível
carro_estado.tentar_alugar()

print("\n--- TESTANDO O PADRÃO DECORATOR ---")

carro = VeiculoFactory.criar_veiculo(
    "carro",
    "ABC1D34",
    Categoria.ECONOMICO,
    taxa_diaria=150.0
)

locacao_base = Locacao(
    veiculo=carro,
    data_inicio=date(2026, 3, 1),
    data_fim=date(2026, 3, 5)
)

print(f"Valor Base (somente diária + seguro base): R$ {locacao_base.calcular_valor_locacao()}")

locacao_com_gps = GPSDecorator(locacao_base)
print(f"Valor somado do pacote + GPS: R$ {locacao_com_gps.calcular_valor_locacao()}")

locacao_vip_top = SeguroTerceirosDecorator(locacao_com_gps)
print(f"Valor pacote completão (Base + GPS + Seg. Terceiros): R$ {locacao_vip_top.calcular_valor_locacao()}")