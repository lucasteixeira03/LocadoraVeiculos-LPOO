import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from control.locacao_controller import LocacaoController
from model.Locacao import Locacao

class JanelaCadastroLocacao(tk.Toplevel):
    def __init__(self, master=None, idLocacao_existente=None):
        super().__init__(master)

        self.idLocacao_existente = idLocacao_existente
        self.title("Atualizar Locação" if idLocacao_existente else "Cadastro de Nova Locação")
        
        self.geometry("450x430")
        self.controller = LocacaoController()

        self.criar_widgets()
        self.carregar_veiculos()
        self.preencher_campos()

    def criar_widgets(self):
        texto_titulo = "Atualizar Locação" if self.idLocacao_existente else "Cadastrar Locação"
        lbl_titulo = tk.Label(self, text=texto_titulo, font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_cliente = tk.Frame(self)
        frame_cliente.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_cliente, text="Cliente:").pack(side="left")
        self.txt_cliente = tk.Entry(frame_cliente)
        self.txt_cliente.pack(side="right", expand=True, fill="x")

        frame_veiculo = tk.Frame(self)
        frame_veiculo.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_veiculo, text="Veículo:").pack(side="left")
        self.cb_veiculo = ttk.Combobox(frame_veiculo, state="readonly")
        self.cb_veiculo.pack(side="right", expand=True, fill="x")

        frame_inicio = tk.Frame(self)
        frame_inicio.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_inicio, text="Data início:").pack(side="left")
        self.txt_data_inicio = tk.Entry(frame_inicio)
        self.txt_data_inicio.pack(side="right", expand=True, fill="x")

        frame_fim = tk.Frame(self)
        frame_fim.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_fim, text="Data fim:").pack(side="left")
        self.txt_data_fim = tk.Entry(frame_fim)
        self.txt_data_fim.pack(side="right", expand=True, fill="x")

        frame_status = tk.Frame(self)
        frame_status.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_status, text="Status:").pack(side="left")
        status_validos = getattr(Locacao, "STATUS_VALIDOS", ("reservado", "locado", "devolvido", "cancelado"))
        self.cb_status = ttk.Combobox(frame_status, values=list(status_validos), state="readonly")
        self.cb_status.current(0)
        self.cb_status.pack(side="right", expand=True, fill="x")

        lbl_ajuda = tk.Label(self, text="Datas: DD/MM/AAAA")
        lbl_ajuda.pack(pady=5)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=20)

        texto_botao = "Atualizar" if self.idLocacao_existente else "Salvar"
        btn_salvar = tk.Button(frame_botoes, text=texto_botao, width=10, command=self.salvar)
        btn_salvar.pack(side="left", padx=5)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", width=10, command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)

    def carregar_veiculos(self):
        placas = self.controller.listar_placas_veiculos()
        self.cb_veiculo["values"] = placas
        if placas:
            self.cb_veiculo.set(placas[0])
        else:
            self.cb_veiculo.set("")
            messagebox.showwarning("Aviso", "Nenhum veículo cadastrado foi encontrado.", parent=self)

    def preencher_campos(self):
        if self.idLocacao_existente is None:
            return

        self.txt_cliente.insert(0, self.idLocacao_existente.cliente)
        self.cb_veiculo.set(self.idLocacao_existente.veiculo.placa)
        self.txt_data_inicio.insert(0, self.idLocacao_existente.data_inicio.strftime("%d/%m/%Y"))
        self.txt_data_fim.insert(0, self.idLocacao_existente.data_fim.strftime("%d/%m/%Y"))
        self.cb_status.set(self.idLocacao_existente.status)

    def salvar(self):
        if self.idLocacao_existente:
            sucesso, msg = self.controller.atualizar_locacao(
                self.idLocacao_existente.id_locacao,
                self.txt_cliente.get().strip(),
                self.cb_veiculo.get().strip(),
                self.txt_data_inicio.get().strip(),
                self.txt_data_fim.get().strip(),
                self.cb_status.get().strip()
            )
        else:
            sucesso, msg = self.controller.salvaLocacao_admin(
                None,
                self.txt_cliente.get().strip(),
                self.cb_veiculo.get().strip(),
                self.txt_data_inicio.get().strip(),
                self.txt_data_fim.get().strip(),
                self.cb_status.get().strip()
            )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
