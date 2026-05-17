import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.locacao_controller import LocacaoController
from model.veiculo import Categoria


class JanelaLocacaoUsuario(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Locação de Veículos")
        self.geometry("900x450")

        self.controller = LocacaoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Locação de Veículos", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Cliente", "Veículo", "Início", "Fim", "Status")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.column("Cliente", width=220)
        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_reserva = tk.Button(frame_botoes, text="Nova Reserva", width=15, command=self.abrir_nova_reserva)
        btn_reserva.pack(side="left", padx=5)

        btn_detalhes = tk.Button(frame_botoes, text="Ver Detalhes", width=15, command=self.ver_detalhes)
        btn_detalhes.pack(side="left", padx=5)

        btn_locar = tk.Button(frame_botoes, text="Locar", width=10, command=self.locar)
        btn_locar.pack(side="left", padx=5)

        btn_devolver = tk.Button(frame_botoes, text="Devolver", width=10, command=self.devolver)
        btn_devolver.pack(side="left", padx=5)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", width=10, command=self.cancelar_reserva)
        btn_cancelar.pack(side="left", padx=5)

        btn_fechar = tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy)
        btn_fechar.pack(side="right", padx=5)

    def abrir_nova_reserva(self):
        janela = JanelaNovaReserva(self)
        self.wait_window(janela)
        self.carregar_dados()

    def ver_detalhes(self):
        locacao = self.__obter_locacao_selecionada()
        if locacao is None:
            return

        detalhes = self.controller.montar_detalhes(locacao)
        messagebox.showinfo("Detalhes da Locação", detalhes, parent=self)

    def locar(self):
        locacao = self.__obter_locacao_selecionada()
        if locacao is None:
            return

        if locacao.status != "reservado":
            messagebox.showwarning("Aviso", "Só é permitido locar reservas.", parent=self)
            return

        sucesso, msg = self.controller.locar(locacao.id_locacao)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def devolver(self):
        locacao = self.__obter_locacao_selecionada()
        if locacao is None:
            return

        if locacao.status != "locado":
            messagebox.showwarning("Aviso", "Só é permitido devolver locações com status locado.", parent=self)
            return

        sucesso, msg, detalhes = self.controller.devolver(locacao.id_locacao)
        if sucesso:
            messagebox.showinfo("Devolução Registrada", detalhes, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def cancelar_reserva(self):
        locacao = self.__obter_locacao_selecionada()
        if locacao is None:
            return

        if locacao.status != "reservado":
            messagebox.showwarning("Aviso", "Só é permitido cancelar reservas.", parent=self)
            return

        sucesso, msg = self.controller.cancelar(locacao.id_locacao)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        locacoes = self.controller.listar_locacoes()
        for locacao in locacoes:
            self.tree.insert("", "end", iid=str(locacao.id_locacao), values=(
                locacao.cliente,
                locacao.veiculo.placa,
                locacao.data_inicio.strftime("%d/%m/%Y"),
                locacao.data_fim.strftime("%d/%m/%Y"),
                locacao.status
            ))

    def __obter_locacao_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação.", parent=self)
            return None

        id_locacao = selecionado[0]
        return self.controller.buscar_por_id(id_locacao)


class JanelaNovaReserva(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Nova Reserva")
        self.geometry("750x500")

        self.controller = LocacaoController()
        self.veiculos = []

        self.criar_widgets()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Nova Reserva", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_cliente = tk.Entry(frame_form)
        self.txt_cliente.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Categoria:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_categoria = ttk.Combobox(frame_form, values=[c.name for c in Categoria], state="readonly")
        self.cb_categoria.current(0)
        self.cb_categoria.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Data início:").grid(row=2, column=0, sticky="w", pady=5)
        self.txt_data_inicio = tk.Entry(frame_form)
        self.txt_data_inicio.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Data fim:").grid(row=3, column=0, sticky="w", pady=5)
        self.txt_data_fim = tk.Entry(frame_form)
        self.txt_data_fim.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        frame_form.columnconfigure(1, weight=1)

        lbl_ajuda = tk.Label(self, text="Datas: DD/MM/AAAA")
        lbl_ajuda.pack(pady=5)

        btn_buscar = tk.Button(self, text="Buscar Veículos Disponíveis", command=self.buscar_veiculos)
        btn_buscar.pack(pady=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Placa", "Tipo", "Categoria", "Taxa Diária")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        btn_salvar = tk.Button(frame_botoes, text="Criar Reserva", width=15, command=self.criar_reserva)
        btn_salvar.pack(side="left", padx=5)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", width=10, command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)

    def buscar_veiculos(self):
        sucesso, msg, veiculos = self.controller.buscar_veiculos_disponiveis(
            self.txt_data_inicio.get().strip(),
            self.txt_data_fim.get().strip(),
            self.cb_categoria.get().strip()
        )

        if not sucesso:
            messagebox.showerror("Erro", msg, parent=self)
            return

        self.veiculos = veiculos
        self.carregar_veiculos()

        if not veiculos:
            messagebox.showinfo("Aviso", "Nenhum veículo disponível para o período.", parent=self)

    def carregar_veiculos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for veiculo in self.veiculos:
            self.tree.insert("", "end", values=(
                veiculo.placa,
                type(veiculo).__name__,
                veiculo.categoria.name,
                f"R$ {veiculo.taxa_diaria:.2f}".replace(".", ",")
            ))

    def criar_reserva(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo disponível.", parent=self)
            return

        item = self.tree.item(selecionado[0])
        placa = item["values"][0]

        sucesso, msg = self.controller.criar_reserva(
            self.txt_cliente.get().strip(),
            placa,
            self.txt_data_inicio.get().strip(),
            self.txt_data_fim.get().strip()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
