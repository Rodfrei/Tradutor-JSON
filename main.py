from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, \
    QCheckBox, QHBoxLayout, QListWidget, QTabWidget, QInputDialog, QComboBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QThread, pyqtSignal
import os
from tradutor import inserir_traducao
from PyQt6.QtGui import QPalette, QColor
import json


def aplicar_tema_escuro(app):
    app.setStyle("Fusion")
    palette = QPalette()

    # Cores principais
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))

    # Links e seleção
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    app.setPalette(palette)

class TraducaoThread(QThread):
    resultado_signal = pyqtSignal(str)

    def __init__(self, entradas, pasta_assets, usar_api, escrever_txt):
        super().__init__()
        self.entradas = entradas
        self.pasta_assets = pasta_assets
        self.usar_api = usar_api
        self.escrever_txt = escrever_txt

    def run(self):
        resultado = inserir_traducao(self.entradas, self.pasta_assets, self.usar_api, self.escrever_txt)
        self.resultado_signal.emit(resultado)


class TradutorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.lista_caminhos = []
        self.caminho_config = os.path.join(os.getcwd(), "config.json")

        self.inicializar_janela()
        self.tabs = QTabWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

        self.criar_aba_json()
        self.criar_aba_config()

    def inicializar_janela(self):
        self.setWindowTitle("Tradutor JSON")
        self.setGeometry(100, 100, 700, 500)
        icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.fonte = QFont("Arial", 14)

    def criar_aba_json(self):
        aba_json = QWidget()
        layout_json = QVBoxLayout()
        aba_json.setLayout(layout_json)

        # Combo de pastas
        self.combo_pastas = QComboBox()
        self.combo_pastas.setFont(self.fonte)
        self.combo_pastas.setMinimumHeight(30)

        # Campos de texto
        self.texto_entrada = self.criar_text_area(False)
        self.resultado_saida = self.criar_text_area(True)
        self.resultado_saida.setReadOnly(True)

        # Botão processar e checkboxes
        self.btn_processar = self.criar_botao("Processar", self.processar_traducoes)
        self.btn_ordenar = self.criar_botao("Ordenar", self.ordenar_jsons)

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.btn_processar)
        layout_botoes.addWidget(self.btn_ordenar)


        self.checkbox_api = self.criar_checkbox(False, "Utilizar API de tradução")
        self.checkbox_txt = self.criar_checkbox(True, "Escrever chaves em .txt")

        widgets = [
            self.criar_label("Pasta dos arquivos JSON:"), self.combo_pastas,
            self.criar_label("Insira os textos (Formato: chave.subchave: valor)"), self.texto_entrada,
            self.criar_layout_checkboxes(), layout_botoes,
            self.criar_label("Resultado:"), self.resultado_saida
        ]

        for widget in widgets:
            if isinstance(widget, QHBoxLayout):
                layout_json.addLayout(widget)
            else:
                layout_json.addWidget(widget)

        self.tabs.addTab(aba_json, "JSON")

    def criar_aba_config(self):
        aba_config = QWidget()
        layout_config = QVBoxLayout()
        aba_config.setLayout(layout_config)

        self.lista_widget = QListWidget()
        self.lista_widget.setFont(self.fonte)
        self.lista_widget.setFixedHeight(130)

        self.carregar_caminhos_salvos()

        btn_adicionar = self.criar_botao("Adicionar", self.adicionar_pasta_config)
        btn_remover = self.criar_botao("Remover", self.remover_caminho)
        btn_guardar = self.criar_botao("Guardar", self.guardar_caminhos)

        label_config = QLabel("Pastas com arquivos JSON:")
        label_config.setFont(self.fonte)
        layout_config.addWidget(label_config)
        layout_config.addWidget(self.lista_widget)
        botoes_layout = QHBoxLayout()
        botoes_layout.addWidget(btn_adicionar)
        botoes_layout.addWidget(btn_guardar)
        botoes_layout.addWidget(btn_remover)
        layout_config.addLayout(botoes_layout)

        layout_config.addStretch()

        self.tabs.addTab(aba_config, "CONFIG")

    def criar_text_area(self, is_read_only):
        text_area = QTextEdit()
        text_area.setFont(self.fonte)
        text_area.setReadOnly(is_read_only)
        text_area.setAcceptRichText(False)
        return text_area

    def criar_label(self, texto):
        label = QLabel(texto)
        label.setFont(self.fonte)
        return label

    def criar_botao(self, texto, funcao):
        botao = QPushButton(texto)
        botao.setFont(self.fonte)
        botao.clicked.connect(funcao)
        return botao

    def criar_checkbox(self, estado, texto):
        checkbox = QCheckBox(texto)
        checkbox.setFont(self.fonte)
        checkbox.setChecked(estado)
        return checkbox

    def criar_layout_checkboxes(self):
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_api)
        layout.addWidget(self.checkbox_txt)
        return layout

    def selecionar_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if pasta_selecionada:
            self.entrada_pasta.setText(pasta_selecionada)

    def processar_traducoes(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self.resultado_saida.setText("Erro: Por favor, selecione a pasta dos arquivos JSON.")
            return

        entradas = self.texto_entrada.toPlainText().strip().split("\n")
        usar_api = self.checkbox_api.isChecked()
        escrever_txt = self.checkbox_txt.isChecked()
        self.resultado_saida.setText("==> Traduzindo...")

        self.thread_traducao = TraducaoThread(entradas, pasta_assets, usar_api, escrever_txt)
        self.thread_traducao.resultado_signal.connect(self.mostrar_resultado)
        self.thread_traducao.start()

    def ordenar_jsons(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self.resultado_saida.setText("Erro: Por favor, selecione a pasta dos arquivos JSON.")
            return

        for lang in ["pt", "en", "es"]:
            caminho = os.path.join(pasta_assets, f"{lang}.json")
            if not os.path.exists(caminho):
                continue
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)

            def ordenar_dict(d):
                if isinstance(d, dict):
                    return {k: ordenar_dict(v) for k, v in sorted(d.items())}
                return d

            dados_ordenados = ordenar_dict(dados)

            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados_ordenados, f, indent=2, ensure_ascii=False)

        self.resultado_saida.setText("Arquivos JSON ordenados com sucesso.")

    def mostrar_resultado(self, resultado):
        self.resultado_saida.setText(resultado)

    def atualizar_combo_pastas(self):
        self.combo_pastas.clear()
        for item in self.lista_caminhos:
            display_text = item['nome']
            self.combo_pastas.addItem(display_text, item['caminho'])

    # Aba config
    def adicionar_pasta_config(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if pasta and not any(item["caminho"] == pasta for item in self.lista_caminhos):
            nome, ok = QInputDialog.getText(self, "Nome da Pasta", "Digite um nome para essa pasta:")
            if ok and nome:
                novo = {"nome": nome, "caminho": pasta}
                self.lista_caminhos.append(novo)
                self.lista_widget.addItem(f"{nome}  →  {pasta}")

    def remover_caminho(self):
        row = self.lista_widget.currentRow()
        if row >= 0:
            self.lista_caminhos.pop(row)
            self.lista_widget.takeItem(row)
        self.atualizar_combo_pastas()

    def guardar_caminhos(self):
        with open(self.caminho_config, "w", encoding="utf-8") as f:
            json.dump(self.lista_caminhos, f, indent=2, ensure_ascii=False)
        self.atualizar_combo_pastas()

    def carregar_caminhos_salvos(self):
        if os.path.exists(self.caminho_config):
            with open(self.caminho_config, "r", encoding="utf-8") as f:
                self.lista_caminhos = json.load(f)
                for item in self.lista_caminhos:
                    self.lista_widget.addItem(f"{item['nome']}  →  {item['caminho']}")
        self.atualizar_combo_pastas()
    ##########################################################


if __name__ == "__main__":
    app = QApplication([])
    icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
    app.setWindowIcon(QIcon(icon_path))
    aplicar_tema_escuro(app)
    window = TradutorApp()
    window.show()
    app.exec()
