import os
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QFileDialog
from PyQt6.QtCore import pyqtSignal
from components import criar_line_edit, criar_lista_widget, criar_label, criar_botao, criar_text_area, limpar_widget_apos

class ConfigTab(QWidget):
    categorias_atualizadas = pyqtSignal(list)
    def __init__(self, caminho_config):
        super().__init__()
        self.caminho_config = caminho_config
        self.lista_caminhos = []
        layout_config = QVBoxLayout()
        self.input_categorias = criar_line_edit(expanding=True)
        self.lista_widget = criar_lista_widget(altura_fixa=130)
        label_config = criar_label("Pastas com arquivos:")
        pesquisa_layout = QHBoxLayout()
        self.input_pesquisa = criar_line_edit(placeholder="Digite para filtrar as pastas...", expanding=True)
        self.input_pesquisa.textChanged.connect(self.filtrar_lista_pastas)
        pesquisa_layout.addWidget(self.input_pesquisa)
        btn_limpar_pesquisa = criar_botao("Limpar", self.limpar_pesquisa)
        pesquisa_layout.addWidget(btn_limpar_pesquisa)
        btn_adicionar = criar_botao("Adicionar", self.adicionar_pasta_config)
        btn_remover = criar_botao("Remover", self.remover_caminho)
        btn_guardar = criar_botao("Guardar", self.guardar_config)
        botoes_layout = QHBoxLayout()
        botoes_layout.addWidget(btn_adicionar)
        botoes_layout.addWidget(btn_remover)
        self.resultado_saida = criar_text_area(is_read_only=True)
        widgets = [
            label_config,
            pesquisa_layout,
            self.lista_widget,
            botoes_layout,
            criar_label("Chaves válidas:"),
            self.input_categorias,
            btn_guardar,
            self.resultado_saida
        ]
        for widget in widgets:
            if hasattr(widget, 'addWidget') or hasattr(widget, 'addLayout'):
                layout_config.addLayout(widget)
            else:
                layout_config.addWidget(widget)
        layout_config.addSpacing(10)
        layout_config.addStretch()
        self.setLayout(layout_config)
        self.carregar_caminhos_salvos()
        self.atualizar_config()
        self.input_categorias.textChanged.connect(self._on_categorias_changed)

    def filtrar_lista_pastas(self):
        termo_pesquisa = self.input_pesquisa.text().strip().lower()
        self.lista_widget.clear()
        for item in self.lista_caminhos:
            nome = item['nome'].lower()
            caminho = item['caminho'].lower()
            if termo_pesquisa == "" or termo_pesquisa in nome or termo_pesquisa in caminho:
                self.lista_widget.addItem(f"{item['nome']}  →  {item['caminho']}")

    def limpar_pesquisa(self):
        self.input_pesquisa.clear()
        self.filtrar_lista_pastas()

    def adicionar_pasta_config(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if pasta and not any(item["caminho"] == pasta for item in self.lista_caminhos):
            nome, ok = QInputDialog.getText(self, "Nome da Pasta", "Digite um nome para essa pasta:")
            if ok and nome:
                novo = {"nome": nome, "caminho": pasta}
                self.lista_caminhos.append(novo)
                self.filtrar_lista_pastas()

    def remover_caminho(self):
        row = self.lista_widget.currentRow()
        if row >= 0:
            item = self.lista_widget.item(row)
            if item:
                item_texto = item.text()
                nome_pasta = item_texto.split("  →  ")[0]
                self.lista_caminhos = [item for item in self.lista_caminhos if item['nome'] != nome_pasta]
                self.filtrar_lista_pastas()
        self.atualizar_config()

    def guardar_config(self):
        categorias_texto = self.input_categorias.text().strip()
        categorias_lista = [cat.strip() for cat in categorias_texto.split(",") if cat.strip()]
        dados = {
            "pastas": self.lista_caminhos,
            "categorias_validas": categorias_lista
        }
        try:
            with open(self.caminho_config, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            limpar_widget_apos(self.resultado_saida, 4000, f"Erro ao salvar configuração: {e}")
            return
        self.atualizar_config()
        limpar_widget_apos(self.resultado_saida, 4000, "Configuração salva com sucesso!")
        self.categorias_atualizadas.emit(categorias_lista)

    def carregar_caminhos_salvos(self):
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.lista_caminhos = dados.get("pastas", [])
                categorias = dados.get("categorias_validas", [])
                self.input_categorias.setText(", ".join(categorias))
                if hasattr(self, 'input_pesquisa'):
                    self.filtrar_lista_pastas()
                else:
                    self.lista_widget.clear()
                    for item in self.lista_caminhos:
                        self.lista_widget.addItem(f"{item['nome']}  →  {item['caminho']}")
            except Exception as e:
                self.lista_caminhos = []
                self.input_categorias.setText("")
                limpar_widget_apos(self.resultado_saida, 4000, f"Erro ao carregar configuração: {e}")
        else:
            self.lista_caminhos = []
            self.input_categorias.setText("utils, tooltip, titulo, menu, mensagem, label, backend")
            if hasattr(self, 'input_pesquisa'):
                self.filtrar_lista_pastas()
            else:
                self.lista_widget.clear()
        self.atualizar_config()

    def atualizar_config(self):
        self.lista_widget.clear()
        for item in self.lista_caminhos:
            self.lista_widget.addItem(f"{item['nome']}  →  {item['caminho']}")

    def _on_categorias_changed(self):
        texto = self.input_categorias.text().strip()
        categorias_lista = [cat.strip() for cat in texto.split(",") if cat.strip()]
        self.categorias_atualizadas.emit(categorias_lista) 