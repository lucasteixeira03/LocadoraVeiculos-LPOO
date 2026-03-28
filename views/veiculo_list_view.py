import tkinter as tk
from tkinter import messagebox

from model.veiculo import Categoria, VeiculoFactory
from views.veiculo_form_view import VeiculoFormView


class VeiculoListView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Locadora de Veiculos")
        self.geometry("700x420")

        self.lista_veiculos = self.criar_lista_inicial()

        self.criar_componentes()

        self.iniciar_listagem()

    def criar_componentes(self):
        self.lbl_titulo = tk.Label(self, text="Veiculos Cadastrados", font=("Arial", 14, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.listbox_veiculos = tk.Listbox(self, width=90, height=14)
        self.listbox_veiculos.pack(padx=10, pady=10, fill="both", expand=True)

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.btn_criar = tk.Button(self.frame_botoes, text="Novo", command=self.abrir_formulario)
        self.btn_criar.pack(side="left", padx=5)

        self.btn_ver = tk.Button(
            self.frame_botoes,
            text="Ver Informacoes",
            command=self.ver_informacoes_veiculo,
        )
        self.btn_ver.pack(side="left", padx=5)
        self.btn_remover = tk.Button(self.frame_botoes, text="Remover", command=self.remover_veiculo)
        self.btn_remover.pack(side="left", padx=5)

    def criar_lista_inicial(self):
        return [
            VeiculoFactory.criar_veiculo("carro", "ABC1D23", Categoria.ECONOMICO, 150.0),
            VeiculoFactory.criar_veiculo("motorhome", "XYZ2E45", Categoria.EXECUTIVO, 420.0),
        ]

    def iniciar_listagem(self):
        self.listbox_veiculos.delete(0, tk.END)

        for veiculo in self.lista_veiculos:
            texto_item = (
                f"Placa: {veiculo.placa} | "
                f"Tipo: {veiculo.__class__.__name__} | "
                f"Categoria: {veiculo.categoria.value} | "
                f"Taxa Diaria: R$ {veiculo.taxa_diaria:.2f}"
            )
            self.listbox_veiculos.insert(tk.END, texto_item)

    def abrir_formulario(self):
        VeiculoFormView(self, self.salvar_novo_veiculo)

    def salvar_novo_veiculo(self, veiculo):
        self.lista_veiculos.append(veiculo)
        self.iniciar_listagem()

    def obter_indice_selecionado(self):
        item_selecionado = self.listbox_veiculos.curselection()

        if not item_selecionado:
            return None

        return item_selecionado[0]

    def ver_informacoes_veiculo(self):
        indice = self.obter_indice_selecionado()

        if indice is None:
            messagebox.showwarning("Selecao obrigatoria", "Selecione um veiculo da lista.")
            return

        veiculo = self.lista_veiculos[indice]
        messagebox.showinfo("Informacoes do Veiculo", veiculo.exibir_dados())

    def remover_veiculo(self):
        indice = self.obter_indice_selecionado()

        if indice is None:
            messagebox.showwarning("Selecao obrigatoria", "Selecione um veiculo para remover.")
            return

        veiculo = self.lista_veiculos[indice]
        confirmar = messagebox.askyesno(
            "Confirmar remocao",
            f"Deseja remover o veiculo {veiculo.placa}?",
        )

        if confirmar:
            del self.lista_veiculos[indice]

            self.iniciar_listagem()


def main():
    app = VeiculoListView()
    app.mainloop()


if __name__ == "__main__":
    main()
