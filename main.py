from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, \
    QCheckBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QThread, pyqtSignal
import os
from tradutor import inserir_traducao


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
        self.inicializar_janela()
        self.layout = QVBoxLayout()
        self.adicionar_widgets()
        self.setLayout(self.layout)

    def inicializar_janela(self):
        self.setWindowTitle("Tradutor JSON")
        self.setGeometry(100, 100, 700, 500)
        icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.fonte = QFont("Arial", 14)

    def adicionar_widgets(self):
        self.entrada_pasta = QLineEdit()
        self.entrada_pasta.setFont(self.fonte)
        self.texto_entrada = self.criar_text_area(False)
        self.resultado_saida = self.criar_text_area(True)
        self.resultado_saida.setReadOnly(True)

        self.btn_selecionar = self.criar_botao("Selecionar", self.selecionar_pasta)
        self.btn_processar = self.criar_botao("Processar", self.processar_traducoes)

        self.checkbox_api = self.criar_checkbox(False, "Utilizar API de tradução")
        self.checkbox_txt = self.criar_checkbox(True, "Escrever chaves em .txt")

        widgets = [
            self.criar_label("Pasta dos arquivos JSON:"), self.entrada_pasta, self.btn_selecionar,
            self.criar_label("Insira os textos (Formato: chave.subchave: valor)"), self.texto_entrada,
            self.criar_layout_checkboxes(), self.btn_processar,
            self.criar_label("Resultado:"), self.resultado_saida
        ]

        for widget in widgets:
            if isinstance(widget, QHBoxLayout):
                self.layout.addLayout(widget)
            else:
                self.layout.addWidget(widget)

    def criar_text_area(self, is_read_only):
        text_area = QTextEdit()
        text_area.setFont(self.fonte)
        text_area.setReadOnly(is_read_only)
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
        pasta_assets = self.entrada_pasta.text()
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

    def mostrar_resultado(self, resultado):
        self.resultado_saida.setText(resultado)


if __name__ == "__main__":
    app = QApplication([])
    icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
    app.setWindowIcon(QIcon(icon_path))
    window = TradutorApp()
    window.show()
    app.exec()
