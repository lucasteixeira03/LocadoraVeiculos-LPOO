import tkinter as tk
from tkinter import messagebox, ttk

from model.veiculo import Categoria, VeiculoFactory


class VeiculoFormView(tk.Toplevel):
    def __init__(self, master, funcao_ao_salvar):
        super().__init__(master)

        self.funcao_ao_salvar = funcao_ao_salvar

        self.title("Cadastro de Veiculo")
        self.geometry("380x260")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.criar_componentes()

    def criar_componentes(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Placa:").grid(row=0, column=0, sticky="w", pady=6)
        self.entry_placa = ttk.Entry(frame)
        self.entry_placa.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(frame, text="Tipo do Veiculo:").grid(row=1, column=0, sticky="w", pady=6)
        self.combo_tipo = ttk.Combobox(frame, state="readonly", values=["Carro", "Motorhome"])
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(frame, text="Categoria:").grid(row=2, column=0, sticky="w", pady=6)
        self.combo_categoria = ttk.Combobox(frame, state="readonly", values=[Categoria.ECONOMICO.value, Categoria.EXECUTIVO.value])
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(frame, text="Taxa Diaria:").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_taxa = ttk.Entry(frame)
        self.entry_taxa.grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Button(frame, text="Salvar", command=self.salvar_veiculo).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(16, 0))

        frame.columnconfigure(1, weight=1)

    def salvar_veiculo(self):
        placa = self.entry_placa.get().strip()
        tipo = self.combo_tipo.get().strip()
        categoria_texto = self.combo_categoria.get().strip()
        taxa_texto = self.entry_taxa.get().strip()

        if not placa or not tipo or not categoria_texto or not taxa_texto:
            messagebox.showerror("Campos obrigatorios", "Preencha todos os campos.")
            return

        try:
            taxa_diaria = float(taxa_texto.replace(",", "."))
        except ValueError:
            messagebox.showerror("Taxa invalida", "Digite uma taxa diaria numerica valida.")
            return

        try:
            categoria = Categoria[categoria_texto]
            veiculo = VeiculoFactory.criar_veiculo(tipo, placa, categoria, taxa_diaria)
        except Exception as erro:
            messagebox.showerror("Erro ao salvar", str(erro))
            return

        self.funcao_ao_salvar(veiculo)

        self.destroy()
