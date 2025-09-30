from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QTabWidget
from PyQt6.QtGui import QIcon
import os
import json
from manual_tab import ManualTab
from unicode_tab import UnicodeTab
from components import aplicar_tema_escuro
from json_tab import JsonTab
from config_tab import ConfigTab
from utils_tab import UtilsTab
from html_tab import HtmlTab


class TradutorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.lista_caminhos = []
        self.caminho_config = os.path.join(os.getcwd(), "config.json")
        self.inicializar_janela()
        self.tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.carregar_configuracoes()
        self.criar_aba_json()
        self.criar_aba_manual()
        self.criar_aba_config()
        self.criar_aba_unicode()
        self.criar_aba_utils()
        self.criar_aba_html()
        self.tabs.currentChanged.connect(self.atualizar_aba_manual)

    def inicializar_janela(self):
        self.setWindowTitle("Tradutor JSON")
        self.setGeometry(0, 0, 960, 500)
        icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
        self.setWindowIcon(QIcon(icon_path))

    def criar_aba_json(self):
        self.json_tab = JsonTab(self.lista_caminhos, self.categorias_validas or [])
        self.tabs.addTab(self.json_tab, "JSON")

    def criar_aba_config(self):
        self.config_tab = ConfigTab(self.caminho_config)
        self.config_tab.categorias_atualizadas.connect(self.atualizar_categorias_validas)
        self.tabs.addTab(self.config_tab, "CONFIG")

    def criar_aba_manual(self):
        def obter_pastas():
            if os.path.exists(self.caminho_config):
                try:
                    with open(self.caminho_config, "r", encoding="utf-8") as f:
                        dados = json.load(f)
                        pastas_salvas = dados.get("pastas", [])
                        return [(item['nome'], item['caminho']) for item in pastas_salvas]
                except Exception:
                    return []
            return []
        self.manual_tab = ManualTab(obter_pastas, self.lista_caminhos, self.categorias_validas or [])
        self.tabs.addTab(self.manual_tab, "MANUAL")

    def criar_aba_unicode(self):
        self.unicode_tab = UnicodeTab()
        self.tabs.addTab(self.unicode_tab, "UNICODE")

    def criar_aba_utils(self):
        self.utils_tab = UtilsTab()
        self.tabs.addTab(self.utils_tab, "UTILS")

    def criar_aba_html(self):
        self.html_tab = HtmlTab()
        self.tabs.addTab(self.html_tab, "HTML")

    def atualizar_aba_manual(self, index):
        tab_text = self.tabs.tabText(index)
        if tab_text == "MANUAL":
            self.manual_tab.atualizar_combo_pastas()

    def selecionar_pasta(self):
        QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        pass

    def carregar_configuracoes(self):
        caminho_config = self.caminho_config
        self.lista_caminhos = []
        self.categorias_validas = []
        if os.path.exists(caminho_config):
            try:
                with open(caminho_config, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.lista_caminhos = dados.get("pastas", [])
                self.categorias_validas = dados.get("categorias_validas", [])
            except Exception:
                self.lista_caminhos = []
                self.categorias_validas = []
        else:
            self.lista_caminhos = []
            self.categorias_validas = ["utils", "tooltip", "titulo", "menu", "mensagem", "label", "backend"]

    def atualizar_categorias_validas(self, categorias):
        categorias = categorias or []
        if hasattr(self, 'json_tab'):
            self.json_tab.set_categorias_validas(categorias)
        if hasattr(self, 'manual_tab'):
            self.manual_tab.set_categorias_validas(categorias)

if __name__ == "__main__":
    app = QApplication([])
    icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
    app.setWindowIcon(QIcon(icon_path))
    aplicar_tema_escuro(app)
    window = TradutorApp()
    window.show()
    app.exec()
