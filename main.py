from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, \
    QCheckBox, QHBoxLayout, QListWidget, QTabWidget, QInputDialog, QComboBox, QSizePolicy
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import os
from tradutor import inserir_traducao
from PyQt6.QtGui import QPalette, QColor
import json
from manual_tab import ManualTab
from unicode_tab import UnicodeTab
from components import criar_lista_widget, criar_combo_box


def aplicar_tema_escuro(app):
    app.setStyle("Fusion")
    palette = QPalette()
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
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)


class TraducaoThread(QThread):
    resultado_signal = pyqtSignal(str)

    def __init__(self, entradas, pasta_assets, usar_api, escrever_txt, atualizar_existente):
        super().__init__()
        self.entradas = entradas
        self.pasta_assets = pasta_assets
        self.usar_api = usar_api
        self.escrever_txt = escrever_txt
        self.atualizar_existente = atualizar_existente

    def run(self):
        resultado = inserir_traducao(
            self.entradas,
            self.pasta_assets,
            self.usar_api,
            self.escrever_txt,
            self.atualizar_existente,
            categorias_validas=None
        )
        self.resultado_signal.emit(resultado)


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
        self.criar_aba_json()
        self.criar_aba_manual()
        self.criar_aba_unicode()
        self.criar_aba_config()
        self.input_categorias.textChanged.connect(self.atualizar_placeholder_texto_entrada)
        self.atualizar_placeholder_texto_entrada()
        self.tabs.currentChanged.connect(self.atualizar_aba_manual)
        self.input_categorias.textChanged.connect(self.atualizar_placeholder_chave_manual)
        self.atualizar_placeholder_chave_manual()

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
        self.combo_pastas = criar_combo_box(fonte=self.fonte)
        self.combo_pastas.setMinimumHeight(30)
        self.texto_entrada = self.criar_text_area(False)
        self.resultado_saida = self.criar_text_area(True)
        self.resultado_saida.setReadOnly(True)
        self.btn_processar = self.criar_botao("Processar", self.processar_traducoes)
        self.btn_ordenar = self.criar_botao("Ordenar", self.ordenar_jsons)
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.btn_processar)
        layout_botoes.addWidget(self.btn_ordenar)
        self.checkbox_api = self.criar_checkbox(False, "Utilizar API")
        self.checkbox_atualizar = self.criar_checkbox(False, "Atualizar existentes")
        self.checkbox_txt = self.criar_checkbox(True, "Escrever em .txt")
        widgets = [
            self.combo_pastas, self.texto_entrada,
            self.criar_layout_checkboxes(), layout_botoes, self.resultado_saida
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
        self.input_categorias = QLineEdit()
        self.input_categorias.setFont(self.fonte)
        self.lista_widget = criar_lista_widget(fonte=self.fonte, altura_fixa=130)
        label_config = QLabel("Pastas com arquivos:")
        label_config.setFont(self.fonte)
        layout_config.addWidget(label_config)
        pesquisa_layout = QHBoxLayout()
        self.input_pesquisa = QLineEdit()
        self.input_pesquisa.setFont(self.fonte)
        self.input_pesquisa.setPlaceholderText("Digite para filtrar as pastas...")
        self.input_pesquisa.textChanged.connect(self.filtrar_lista_pastas)
        pesquisa_layout.addWidget(self.input_pesquisa)
        btn_limpar_pesquisa = self.criar_botao("Limpar", self.limpar_pesquisa)
        pesquisa_layout.addWidget(btn_limpar_pesquisa)
        layout_config.addLayout(pesquisa_layout)
        layout_config.addWidget(self.lista_widget)
        btn_adicionar = self.criar_botao("Adicionar", self.adicionar_pasta_config)
        btn_remover = self.criar_botao("Remover", self.remover_caminho)
        btn_guardar = self.criar_botao("Guardar", self.guardar_config)
        botoes_layout = QHBoxLayout()
        botoes_layout.addWidget(btn_adicionar)
        botoes_layout.addWidget(btn_remover)
        layout_config.addLayout(botoes_layout)
        layout_config.addWidget(self.criar_label("Chaves válidas:"))
        layout_config.addWidget(self.input_categorias)
        layout_config.addSpacing(10)
        layout_config.addWidget(btn_guardar)
        layout_config.addStretch()
        self.tabs.addTab(aba_config, "CONFIG")
        self.carregar_caminhos_salvos()
        self.atualizar_config()

    def criar_layout_checkboxes(self):
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_api)
        layout.addWidget(self.checkbox_atualizar)
        layout.addWidget(self.checkbox_txt)
        return layout

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
        self.manual_tab = ManualTab(obter_pastas)
        self.tabs.addTab(self.manual_tab, "MANUAL")

    def criar_aba_unicode(self):
        self.unicode_tab = UnicodeTab()
        self.tabs.addTab(self.unicode_tab, "UNICODE")

    def atualizar_aba_manual(self, index):
        tab_text = self.tabs.tabText(index)
        if tab_text == "MANUAL":
            self.manual_tab.atualizar_combo_pastas()
            self.atualizar_placeholder_chave_manual()

    def selecionar_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        pass

    def atualizar_placeholder_texto_entrada(self):
        categorias = self.input_categorias.text().strip()
        if categorias == "":
            self.texto_entrada.setPlaceholderText("chave: valor")
        else:
            self.texto_entrada.setPlaceholderText("chave.subchave: valor")

    def atualizar_placeholder_chave_manual(self):
        categorias = self.input_categorias.text().strip()
        if hasattr(self, 'manual_tab'):
            if categorias == "":
                self.manual_tab.input_chave.setPlaceholderText("chave")
            else:
                self.manual_tab.input_chave.setPlaceholderText("chave.subchave")

    def processar_traducoes(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self.resultado_saida.setText("⚠️ Selecione uma pasta de arquivos JSON para continuar.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        usar_api = self.checkbox_api.isChecked()
        escrever_txt = self.checkbox_txt.isChecked()
        atualizar_existente = self.checkbox_atualizar.isChecked()
        self.resultado_saida.setText("🔄 Processando traduções...")
        entradas = self.texto_entrada.toPlainText().strip().split("\n")
        entradas = [entrada.strip() for entrada in entradas if entrada.strip()]
        if not entradas:
            self.resultado_saida.setText("⚠️ Nenhum texto para processar. Digite algo no campo de entrada.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        categorias_validas = [cat.strip() for cat in self.input_categorias.text().strip().split(",") if cat.strip()]
        if not categorias_validas:
            entradas_formatadas = []
            for texto in entradas:
                if ":" not in texto:
                    self.resultado_saida.setText(f"❌ Formato inválido: '{texto.strip()}' (formato esperado: chave: valor)")
                    QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
                    return
                chave, valor = texto.split(":", 1)
                chave = chave.strip()
                valor = valor.strip()
                if not chave:
                    self.resultado_saida.setText(f"❌ Chave vazia na linha: '{texto.strip()}'")
                    QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
                    return
                entradas_formatadas.append(f"{chave}: {valor}")
            self.thread_traducao = TraducaoThread(entradas_formatadas, pasta_assets, usar_api, escrever_txt, atualizar_existente)
            self.thread_traducao.resultado_signal.connect(self.mostrar_resultado)
            self.thread_traducao.start()
        else:
            self.thread_traducao = TraducaoThread(entradas, pasta_assets, usar_api, escrever_txt, atualizar_existente)
            self.thread_traducao.resultado_signal.connect(self.mostrar_resultado)
            self.thread_traducao.start()

    def ordenar_jsons(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self.resultado_saida.setText("⚠️ Selecione uma pasta de arquivos JSON para continuar.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        self.resultado_saida.setText("🔄 Ordenando arquivos JSON...")
        for lang in ["pt", "en", "es"]:
            caminho = os.path.join(pasta_assets, f"{lang}.json")
            if not os.path.exists(caminho):
                continue
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception as e:
                self.resultado_saida.setText(f"❌ Erro ao ler {lang}.json: {e}")
                QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
                continue
            def ordenar_dict(d):
                if isinstance(d, dict):
                    return {k: ordenar_dict(v) for k, v in sorted(d.items())}
                return d
            dados_ordenados = ordenar_dict(dados)
            try:
                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(dados_ordenados, f, indent=2, ensure_ascii=False)
            except Exception as e:
                self.resultado_saida.setText(f"❌ Erro ao salvar {lang}.json: {e}")
                QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
                continue
        self.resultado_saida.setText("✅ Arquivos JSON ordenados com sucesso!")
        QTimer.singleShot(4000, lambda: self.resultado_saida.clear())

    def mostrar_resultado(self, resultado):
        self.resultado_saida.setText(resultado)
        QTimer.singleShot(4000, lambda: self.resultado_saida.clear())

    def atualizar_config(self):
        self.combo_pastas.clear()
        for item in self.lista_caminhos:
            display_text = item['nome']
            self.combo_pastas.addItem(display_text, item['caminho'])

    def filtrar_lista_pastas(self):
        if not hasattr(self, 'input_pesquisa'):
            return
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
            self.resultado_saida.setText(f"❌ Erro ao salvar configuração: {e}")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        self.atualizar_config()
        if hasattr(self, 'manual_tab'):
            self.manual_tab.atualizar_combo_pastas()

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
                self.resultado_saida.setText(f"❌ Erro ao carregar configuração: {e}")
                QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
        else:
            self.lista_caminhos = []
            self.input_categorias.setText("utils, tooltip, titulo, menu, mensagem, label, backend")
            if hasattr(self, 'input_pesquisa'):
                self.filtrar_lista_pastas()
            else:
                self.lista_widget.clear()
        self.atualizar_config()

if __name__ == "__main__":
    app = QApplication([])
    icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
    app.setWindowIcon(QIcon(icon_path))
    aplicar_tema_escuro(app)
    window = TradutorApp()
    window.show()
    app.exec()
