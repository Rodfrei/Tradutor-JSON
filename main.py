from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, QCheckBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QThread, pyqtSignal
import os
from tradutor import inserir_traducao

class TraducaoThread(QThread):
    resultado_signal = pyqtSignal(str)

    def __init__(self, entradas, pasta_assets, usar_api):
        super().__init__()
        self.entradas = entradas
        self.pasta_assets = pasta_assets
        self.usar_api = usar_api

    def run(self):
        resultado = inserir_traducao(self.entradas, self.pasta_assets, self.usar_api)
        self.resultado_signal.emit(resultado)

class TradutorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tradutor JSON")
        self.setGeometry(100, 100, 700, 500)
        icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.layout = QVBoxLayout()
        fonte = QFont("Arial", 14)

        self.label_pasta = QLabel("Pasta dos arquivos JSON:")
        self.label_pasta.setFont(fonte)
        self.layout.addWidget(self.label_pasta)

        self.entrada_pasta = QLineEdit()
        self.entrada_pasta.setFont(fonte)
        self.layout.addWidget(self.entrada_pasta)

        self.btn_selecionar = QPushButton("Selecionar")
        self.btn_selecionar.setFont(fonte)
        self.btn_selecionar.clicked.connect(self.selecionar_pasta)
        self.layout.addWidget(self.btn_selecionar)

        self.label_entrada = QLabel("Insira os textos (Formato: chave.subchave: valor)")
        self.label_entrada.setFont(fonte)
        self.layout.addWidget(self.label_entrada)

        self.texto_entrada = QTextEdit()
        self.texto_entrada.setFont(fonte)
        self.layout.addWidget(self.texto_entrada)

        self.checkbox_api = QCheckBox("Utilizar API de tradução")
        self.checkbox_api.setFont(fonte)
        self.layout.addWidget(self.checkbox_api)

        self.btn_processar = QPushButton("Processar Traduções")
        self.btn_processar.setFont(fonte)
        self.btn_processar.clicked.connect(self.processar_traducoes)
        self.layout.addWidget(self.btn_processar)

        self.label_resultado = QLabel("Resultados:")
        self.label_resultado.setFont(fonte)
        self.layout.addWidget(self.label_resultado)

        self.resultado_saida = QTextEdit()
        self.resultado_saida.setFont(fonte)
        self.resultado_saida.setReadOnly(True)
        self.layout.addWidget(self.resultado_saida)

        self.setLayout(self.layout)

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
        self.resultado_saida.setText("==> Traduzindo...")

        self.thread_traducao = TraducaoThread(entradas, pasta_assets, usar_api)
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
