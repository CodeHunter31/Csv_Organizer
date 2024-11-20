import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de CSV com Tabelas Dinâmicas")
        self.root.geometry("800x600")

        # Variáveis
        self.df = None

        # Frame superior para botões
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Botão para carregar CSV
        load_button = ttk.Button(top_frame, text="Carregar CSV", command=self.load_csv)
        load_button.pack(side=tk.LEFT, padx=5)

        # Botão para exportar 
        export_button = ttk.Button(top_frame, text="Exclaerportar CSV", command=self.export_csv)
        export_button.pack(side=tk.LEFT, padx=5)

        # Dropdown para selecionar colunas
        self.filter_var = tk.StringVar(value="Selecione uma coluna")
        self.filter_dropdown = ttk.Combobox(top_frame, textvariable=self.filter_var, state="readonly")
        self.filter_dropdown.pack(side=tk.LEFT, padx=5)

        # Entrada para filtro
        self.filter_entry = ttk.Entry(top_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        # Botão para aplicar filtro
        filter_button = ttk.Button(top_frame, text="Filtrar", command=self.apply_filter)
        filter_button.pack(side=tk.LEFT, padx=5)

        # Frame para tabela
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Inicializa tabela vazia
        self.tree = ttk.Treeview(self.table_frame, columns=[], show='headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_csv(self):
        """Carrega um arquivo CSV e exibe os dados na tabela."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            self.df = pd.read_csv(file_path)
            self.update_table(self.df)
            self.filter_dropdown['values'] = list(self.df.columns)
            self.filter_var.set("Selecione uma coluna")
            messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

    def update_table(self, dataframe):
        """Atualiza a tabela com os dados de um DataFrame."""
        # Limpa a tabela existente
        for col in self.tree.get_children():
            self.tree.delete(col)
        self.tree["columns"] = list(dataframe.columns)
        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Adiciona os dados
        for _, row in dataframe.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def apply_filter(self):
        """Aplica o filtro na tabela com base na coluna e valor fornecidos."""
        if self.df is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
            return

        column = self.filter_var.get()
        if column == "Selecione uma coluna" or not self.filter_entry.get():
            messagebox.showwarning("Aviso", "Selecione uma coluna e insira um valor para filtrar.")
            return

        value = self.filter_entry.get()
        filtered_df = self.df[self.df[column].astype(str).str.contains(value, na=False, case=False)]
        self.update_table(filtered_df)

    def export_csv(self):
        """Exporta os dados atualmente exibidos na tabela para um novo arquivo CSV."""
        if self.df is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            # Obtém os dados visíveis na tabela
            data = [self.tree.item(row)['values'] for row in self.tree.get_children()]
            visible_df = pd.DataFrame(data, columns=self.df.columns)
            visible_df.to_csv(file_path, index=False)
            messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar o arquivo: {e}")

# Inicializa o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
