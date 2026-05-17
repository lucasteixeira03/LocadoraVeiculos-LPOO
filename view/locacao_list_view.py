import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.locacao_controller import LocacaoController

class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Locações Cadastradas")
        self.geometry("900x450")

        self.controller = LocacaoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Locações Cadastradas", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Cliente", "Veículo", "Início", "Fim", "Status", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=110)

        self.tree.column("Cliente", width=180)
        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_novo = tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo)
        btn_novo.pack(side="left", padx=5)

        btn_editar = tk.Button(frame_botoes, text="Editar", width=10, command=self.abrir_editar)
        btn_editar.pack(side="left", padx=5)

        btn_remover = tk.Button(frame_botoes, text="Remover", width=10, command=self.remover_locacao)
        btn_remover.pack(side="left", padx=5)

        btn_detalhes = tk.Button(frame_botoes, text="Ver Detalhes", width=15, command=self.ver_detalhes)
        btn_detalhes.pack(side="left", padx=5)

        btn_fechar = tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy)
        btn_fechar.pack(side="right", padx=5)

    def abrir_novo(self):
        from view.locacao_view import JanelaCadastroLocacao
        janela = JanelaCadastroLocacao(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_locacao = self.__obter_id_selecionado()
        if id_locacao is None:
            return

        locacao = self.controller.buscar_por_id(id_locacao)
        if locacao is None:
            messagebox.showerror("Erro", "Locação não encontrada.", parent=self)
            return

        from view.locacao_view import JanelaCadastroLocacao
        janela = JanelaCadastroLocacao(self, idLocacao_existente=locacao)
        self.wait_window(janela)
        self.carregar_dados()

    def remover_locacao(self):
        id_locacao = self.__obter_id_selecionado()
        if id_locacao is None:
            return

        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja remover a locação {id_locacao}?",
            parent=self
        )
        if resposta:
            sucesso, msg = self.controller.remover_locacao(id_locacao)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def ver_detalhes(self):
        id_locacao = self.__obter_id_selecionado()
        if id_locacao is None:
            return

        locacao = self.controller.buscar_por_id(id_locacao)
        detalhes = self.controller.montar_detalhes(locacao)
        messagebox.showinfo("Detalhes da Locação", detalhes, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        locacoes = self.controller.listar_locacoes()
        for locacao in locacoes:
            valor = ""
            if locacao.valor_total is not None:
                valor = f"R$ {locacao.valor_total:.2f}".replace(".", ",")

            self.tree.insert("", "end", iid=str(locacao.id_locacao), values=(
                locacao.cliente,
                locacao.veiculo.placa,
                locacao.data_inicio.strftime("%d/%m/%Y"),
                locacao.data_fim.strftime("%d/%m/%Y"),
                locacao.status,
                valor
            ))

    def __obter_id_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação.", parent=self)
            return None

        return selecionado[0]
