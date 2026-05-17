import tkinter as tk
import sys
import os

# Adiciona o diretório raiz ao sys.path para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from view.veiculo_list_view import JanelaListagemVeiculos
from view.locacao_list_view import JanelaListagemLocacoes
from view.locacao_usuario_view import JanelaLocacaoUsuario
from model.veiculo import VeiculoFactory, Categoria
import view.veiculo_list_view as list_view

def popular_dados_iniciais():
    """Popula a lista com alguns dados iniciais para testar a interface."""
    v1 = VeiculoFactory.criar_veiculo("carro", "ABC1D23", Categoria.ECONOMICO, 150.0)
    v2 = VeiculoFactory.criar_veiculo("motorhome", "XYZ9A99", Categoria.EXECUTIVO, 300.0)
    list_view.lista_veiculos.extend([v1, v2])


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Locadora de Veículos")
        self.geometry("500x300")
        self.criar_menu()
        self.criar_widgets()

    def criar_menu(self):
        barra_menu = tk.Menu(self)

        menu_cadastro = tk.Menu(barra_menu, tearoff=0)
        menu_cadastro.add_command(label="Veículo", command=self.abrir_veiculos)
        menu_cadastro.add_command(label="Locações", command=self.abrir_locacoes_admin)
        barra_menu.add_cascade(label="Cadastro", menu=menu_cadastro)

        menu_acao = tk.Menu(barra_menu, tearoff=0)
        menu_acao.add_command(label="Locar Veículo", command=self.abrir_locacao_usuario)
        barra_menu.add_cascade(label="Ação", menu=menu_acao)

        self.config(menu=barra_menu)

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Sistema de Locadora de Veículos", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=60)

        lbl_info = tk.Label(self, text="Use os menus Cadastro e Ação para acessar as telas.")
        lbl_info.pack(pady=10)

    def abrir_veiculos(self):
        JanelaListagemVeiculos(self)

    def abrir_locacoes_admin(self):
        JanelaListagemLocacoes(self)

    def abrir_locacao_usuario(self):
        JanelaLocacaoUsuario(self)

if __name__ == "__main__":
    #popular_dados_iniciais()

    app = JanelaPrincipal()
    app.mainloop()
