from datetime import date, datetime
from dao.locacao_dao import LocacaoDAO
from dao.veiculo_dao import VeiculoDAO
from model.Locacao import Locacao

class LocacaoController:
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.veiculo_dao = VeiculoDAO()

    def listar_locacoes(self):
        try:
            return self.locacao_dao.listar_todos()
        
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return None

    def buscar_por_id(self, id_locacao):
        try:
            return self.locacao_dao.buscar_por_id(id_locacao)
        
        except Exception as e:
            print(f"Erro ao buscar locação: {e}")
            return None

    def listar_veiculos(self):
        try:
            return self.veiculo_dao.listar_todos()
        
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return None

    def listar_placas_veiculos(self):
        try:
            return self.veiculo_dao.listar_placas()
        
        except Exception as e:
            print(f"Erro ao listar placas dos veículos: {e}")
            return None

    def buscar_veiculos_disponiveis(self, data_inicio_str, data_fim_str, categoria_str):
        try:
            data_inicio = self.__converteDataBD(data_inicio_str)
            data_fim = self.__converteDataBD(data_fim_str)
            if data_inicio > data_fim:
                return False, "Data de início deve ser menor ou igual à data de fim", []

            veiculos = self.locacao_dao.buscar_veiculos_disponiveis(data_inicio, data_fim, categoria_str.strip().upper())
            return True, "Busca realizada com sucesso", veiculos
        
        except Exception as e:
            return False, f"Erro ao buscar veículos disponíveis: {e}", []

    def criar_reserva(self, cliente, placa, data_inicio_str, data_fim_str):
        if not cliente or not placa or not data_inicio_str or not data_fim_str:
            return False, "Preencha todos os campos"

        try:
            data_inicio = self.__converteDataBD(data_inicio_str)
            data_fim = self.__converteDataBD(data_fim_str)

            if data_inicio > data_fim:
                return False, "Data de início deve ser menor ou igual à data de fim"

            if self.locacao_dao.existe_conflito(placa, data_inicio, data_fim):
                return False, "Veículo indisponível para o período informado"

            veiculo = self.veiculo_dao.buscar_por_placa(placa)
            if veiculo is None:
                return False, "Veículo não encontrado"

            locacao = Locacao(
                veiculo=veiculo,
                cliente=cliente.strip(),
                data_inicio=data_inicio,
                data_fim=data_fim,
                status="reservado"
            )
            locacao.valor_total = locacao.calcular_valor_locacao()

            return self.locacao_dao.salvar(locacao)
        
        except Exception as e:
            return False, f"Erro ao criar reserva: {e}"

    def salvaLocacao_admin(self, id_locacao, cliente, placa, data_inicio_str, data_fim_str, status):
        if id_locacao:
            return self.atualizar_locacao(id_locacao, cliente, placa, data_inicio_str, data_fim_str, status)

        if not cliente or not placa or not data_inicio_str or not data_fim_str or not status:
            return False, "Preencha todos os campos obrigatórios"

        try:
            data_inicio = self.__converteDataBD(data_inicio_str)
            data_fim = self.__converteDataBD(data_fim_str)

            if data_inicio > data_fim:
                return False, "Data de início deve ser anterior ou igual à data de fim"

            veiculo = self.veiculo_dao.buscar_por_placa(placa)
            if veiculo is None:
                return False, "Veículo não encontrado"

            locacao = Locacao(
                veiculo=veiculo,
                cliente=cliente.strip(),
                data_inicio=data_inicio,
                data_fim=data_fim,
                status=status
            )
            locacao.valor_total = locacao.calcular_valor_locacao()

            return self.locacao_dao.salvar(locacao)
        
        except ValueError as e:
            return False, f"Valor inválido: {e}"
        
        except Exception as e:
            return False, f"Erro ao salvar locação: {e}"

    def atualizar_locacao(self, id_locacao, cliente, placa, data_inicio_str, data_fim_str, status):
        if not id_locacao or not cliente or not placa or not data_inicio_str or not data_fim_str or not status:
            return False, "Preencha todos os campos obrigatórios"

        try:
            idLocacao_existente = self.locacao_dao.buscar_por_id(id_locacao)
            if not idLocacao_existente:
                return False, f"Locação com código {id_locacao} não foi encontrada"

            data_inicio = self.__converteDataBD(data_inicio_str)
            data_fim = self.__converteDataBD(data_fim_str)

            if data_inicio > data_fim:
                return False, "Data de início deve ser anterior ou igual à data de fim"

            veiculo = self.veiculo_dao.buscar_por_placa(placa)
            if veiculo is None:
                return False, "Veículo não encontrado"

            locacao_atualizada = Locacao(
                veiculo=veiculo,
                cliente=cliente.strip(),
                data_inicio=data_inicio,
                data_fim=data_fim,
                status=status,
                id_locacao= id_locacao
            )
            locacao_atualizada.valor_total = locacao_atualizada.calcular_valor_locacao()

            return self.locacao_dao.atualizar(locacao_atualizada)
        
        except ValueError as e:
            return False, f"Valor inválido: {e}"
        
        except Exception as e:
            return False, f"Erro ao atualizar locação: {e}"

    def remover_locacao(self, id_locacao):
        if not id_locacao:
            return False, "Código da locação não informado"

        try:
            return self.locacao_dao.remover(id_locacao)
        
        except Exception as e:
            return False, f"Erro ao remover locação: {e}"

    def locar(self, id_locacao):
        idLocacao = self.buscar_por_id(id_locacao)
        if idLocacao is None:
            return False, "Locação não encontrada"

        if idLocacao.status != "reservado":
            return False, "Somente reservas podem ser locadas"

        daHoje = date.today()
        if idLocacao.data_fim < daHoje:
            return False, "A data de fim prevista já passou. Ajuste a locação no cadastro administrativo."

        if idLocacao.data_inicio != daHoje:
            idLocacao.data_inicio = daHoje

        idLocacao.status = "locado"
        return self.locacao_dao.atualizar(idLocacao)

    def devolver(self, id_locacao):
        idLocacao = self.buscar_por_id(id_locacao)
        if idLocacao is None:
            return False, "Locação não encontrada", None

        if idLocacao.status != "locado":
            return False, "Somente locações em andamento podem ser devolvidas", None

        daHoje = date.today()
        if idLocacao.data_inicio >= daHoje:
            return False, "A devolução só é permitida se a data de início for anterior à data atual", None

        idLocacao.data_fim = daHoje
        idLocacao.status = "devolvido"
        idLocacao.valor_total = idLocacao.calcular_valor_locacao()

        sucesso, msg = self.locacao_dao.atualizar(idLocacao)
        if sucesso:
            return True, msg, self.montar_detalhes(idLocacao)
        return False, msg, None

    def cancelar(self, id_locacao):
        idLocacao = self.buscar_por_id(id_locacao)
        if idLocacao is None:
            return False, "Locação não encontrada"

        if idLocacao.status != "reservado":
            return False, "Somente reservas podem ser canceladas"

        idLocacao.status = "cancelado"
        return self.locacao_dao.atualizar(idLocacao)

    def montar_detalhes(self, locacao):
        if locacao is None:
            return "Locação não encontrada."

        detalhes = [
            f"Código: {locacao.id_locacao}",
            f"Cliente: {locacao.cliente}",
            f"Veículo: {locacao.veiculo.placa}",
            f"Status: {locacao.status}"
        ]

        if locacao.status == "cancelado":
            detalhes.append("Esta locação foi cancelada.")
            return "\n".join(detalhes)

        dias = locacao.calcular_diarias()
        valor = locacao.valor_total
        if valor is None:
            valor = locacao.calcular_valor_locacao()

        if locacao.status == "devolvido":
            detalhes.append(f"Data de início: {self.__formatarDataBD(locacao.data_inicio)}")
            detalhes.append(f"Data de devolução: {self.__formatarDataBD(locacao.data_fim)}")
            detalhes.append(f"Número de diárias: {dias}")
            detalhes.append(f"Valor total: R$ {valor:.2f}")
        else:
            detalhes.append(f"Data de início: {self.__formatarDataBD(locacao.data_inicio)}")
            detalhes.append(f"Data de fim prevista: {self.__formatarDataBD(locacao.data_fim)}")
            detalhes.append(f"Valor estimado: R$ {valor:.2f}")

        return "\n".join(detalhes)

    def __converteDataBD(self, texto):
        texto = texto.strip()
        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Use a data no formato DD/MM/AAAA")

    def __formatarDataBD(self, data):
        if data is None:
            return ""
        return data.strftime("%d/%m/%Y")
