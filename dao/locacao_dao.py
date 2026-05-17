import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Locacao import *
from model.veiculo import VeiculoFactory, Categoria
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO

class LocacaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, objeto: Locacao):
        if not self.conexao:
            raise Exception("Sem conexão com o BD")
        
        try:
            cursor = self.conexao.cursor()
            query = """INSERT INTO tb_locacao
            (loc_vei_placa, loc_cliente, loc_data_inicio, loc_data_fim, loc_status, loc_valor)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING loc_id"""
            cursor.execute(query, (objeto.veiculo.placa,
                                   objeto.cliente,
                                   objeto.data_inicio,
                                   objeto.data_fim,
                                   objeto.status,
                                   objeto.valor_total))
            objeto.id_locacao = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Locação cadastrada com sucesso"
        
        except Exception as e:
            print(f"Erro ao inserir locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao inserir locação: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, objeto: Locacao):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_locacao
                    SET loc_vei_placa = %s, loc_cliente = %s, loc_data_inicio = %s,
                        loc_data_fim = %s, loc_status = %s, loc_valor = %s
                    WHERE loc_id = %s"""
            cursor.execute(query, (objeto.veiculo.placa,
                                   objeto.cliente,
                                   objeto.data_inicio,
                                   objeto.data_fim,
                                   objeto.status,
                                   objeto.valor_total,
                                   objeto.id_locacao))
            self.conexao.commit()
            return True, "Locação atualizada com sucesso"
        
        except Exception as e:
            print(f"Erro ao atualizar locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar locação: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_objeto):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_locacao WHERE loc_id = %s"
            cursor.execute(query, (id_objeto,))
            self.conexao.commit()
            return True, "Locação removida com sucesso"
        
        except Exception as e:
            print(f"Erro ao remover locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover locação: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = """SELECT l.loc_id, l.loc_cliente, l.loc_data_inicio, l.loc_data_fim, l.loc_status, l.loc_valor,
                   v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria
            FROM tb_locacao l
            INNER JOIN tb_veiculos v ON v.vei_placa = l.loc_vei_placa
            ORDER BY l.loc_id
            """
            cursor.execute(query)
            linhas = cursor.fetchall()
            return [self.__montar_locacao(linha) for linha in linhas]
        
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_locacao):
        if not self.conexao:
            return None

        try:
            cursor = self.conexao.cursor()
            query = """SELECT l.loc_id, l.loc_cliente, l.loc_data_inicio, l.loc_data_fim, l.loc_status, l.loc_valor,
                   v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria
            FROM tb_locacao l
            INNER JOIN tb_veiculos v ON v.vei_placa = l.loc_vei_placa
            WHERE l.loc_id = %s
            """
            cursor.execute(query, (id_locacao,))
            linha = cursor.fetchone()

            if linha:
                return self.__montar_locacao(linha)
            
            return None
        
        except Exception as e:
            print(f"Erro ao buscar locação: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()

    def existe_conflito(self, placa, data_inicio, data_fim, id_locacao=None):
        if not self.conexao:
            return False
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT COUNT(*)
            FROM tb_locacao
            WHERE loc_vei_placa = %s AND LOWER(loc_status) IN ('reservado', 'locado') AND NOT (loc_data_fim < %s OR loc_data_inicio > %s)"""
            parametros = [placa, data_inicio, data_fim]

            if id_locacao is not None:
                query += " AND loc_id <> %s"
                parametros.append(id_locacao)

            cursor.execute(query, tuple(parametros))
            total = cursor.fetchone()[0]
            return total > 0
        
        except Exception as e:
            print(f"Erro ao verificar conflito de locação: {e}")
            return False
        
        finally:
            if cursor:
                cursor.close()

    def buscar_veiculos_disponiveis(self, data_inicio, data_fim, categoria):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria
            FROM tb_veiculos v
            WHERE v.vei_categoria = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM tb_locacao l
                  WHERE l.loc_vei_placa = v.vei_placa AND LOWER(l.loc_status) IN ('reservado', 'locado') AND NOT (l.loc_data_fim < %s OR l.loc_data_inicio > %s)
                  )
            ORDER BY v.vei_placa"""
            cursor.execute(query, (categoria, data_inicio, data_fim))
            linhas = cursor.fetchall()
            veiculos = []
            for linha in linhas:
                veiculos.append(VeiculoFactory.criar_veiculo(linha[0], linha[1], Categoria[linha[2]], float(linha[3])))
            return veiculos
        
        except Exception as e:
            print(f"Erro ao buscar veículos disponíveis: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def __montar_locacao(self, linha):
        veiculo = VeiculoFactory.criar_veiculo(linha[6], linha[7], Categoria[linha[8]], float(linha[9]))
        return Locacao(
            veiculo=veiculo,
            data_inicio=linha[2],
            data_fim=linha[3],
            id_locacao=linha[0],
            cliente=linha[1] or "",
            status=linha[4],
            valor_total=float(linha[5]) if linha[5] is not None else None
        )
