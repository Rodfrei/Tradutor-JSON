from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, \
    QCheckBox, QHBoxLayout, QListWidget, QTabWidget, QInputDialog, QComboBox, QSizePolicy
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import os
from tradutor import inserir_traducao
from PyQt6.QtGui import QPalette, QColor
import json
from manual_tab import ManualTab


def aplicar_tema_escuro(app):
    """Aplica o tema escuro à aplicação Qt."""
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
    """Thread para processar traduções sem travar a interface."""
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
    """Janela principal do Tradutor JSON."""
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
        self.criar_aba_config()
        self.input_categorias.textChanged.connect(self.atualizar_placeholder_texto_entrada)
        self.atualizar_placeholder_texto_entrada()
        # Atualiza combo de pastas da aba MANUAL ao selecionar a aba
        self.tabs.currentChanged.connect(self.atualizar_aba_manual)
        # Atualiza placeholder do campo de chave da aba MANUAL
        self.input_categorias.textChanged.connect(self.atualizar_placeholder_chave_manual)
        self.atualizar_placeholder_chave_manual()  # Agora é seguro chamar aqui

    def inicializar_janela(self):
        """Configura propriedades da janela principal."""
        self.setWindowTitle("Tradutor JSON")
        self.setGeometry(100, 100, 700, 500)
        icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.fonte = QFont("Arial", 14)

    def criar_aba_json(self):
        """Cria a aba principal de tradução de JSON."""
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
        # Botões e checkboxes
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
        # Removido: atualização do placeholder e conexão do sinal

    def criar_aba_config(self):
        """Cria a aba de configuração de pastas e categorias."""
        aba_config = QWidget()
        layout_config = QVBoxLayout()
        aba_config.setLayout(layout_config)
        self.input_categorias = QLineEdit()
        self.input_categorias.setFont(self.fonte)
        self.lista_widget = QListWidget()
        self.lista_widget.setFont(self.fonte)
        self.lista_widget.setFixedHeight(130)
        self.carregar_caminhos_salvos()
        label_config = QLabel("Pastas com arquivos pt.json, en.json, es.json:")
        label_config.setFont(self.fonte)
        layout_config.addWidget(label_config)
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

    def criar_text_area(self, is_read_only):
        """Cria um campo de texto configurado."""
        text_area = QTextEdit()
        text_area.setFont(self.fonte)
        text_area.setReadOnly(is_read_only)
        text_area.setAcceptRichText(False)
        if is_read_only:
            text_area.setFixedHeight(80)
            text_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        else:
            text_area.setPlaceholderText("chave.subchave: valor")
        return text_area

    def criar_label(self, texto):
        """Cria um QLabel com fonte padrão."""
        label = QLabel(texto)
        label.setFont(self.fonte)
        return label

    def criar_botao(self, texto, funcao):
        """Cria um QPushButton com fonte padrão e conecta a função."""
        botao = QPushButton(texto)
        botao.setFont(self.fonte)
        botao.clicked.connect(funcao)
        return botao

    def criar_checkbox(self, estado, texto):
        """Cria um QCheckBox com fonte padrão."""
        checkbox = QCheckBox(texto)
        checkbox.setFont(self.fonte)
        checkbox.setChecked(estado)
        return checkbox

    def criar_layout_checkboxes(self):
        """Agrupa os checkboxes em um layout horizontal."""
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_api)
        layout.addWidget(self.checkbox_atualizar)
        layout.addWidget(self.checkbox_txt)
        return layout

    def criar_aba_manual(self):
        """Cria a aba MANUAL e adiciona ao QTabWidget."""
        def obter_pastas():
            # Retorna apenas as pastas salvas no arquivo config.json
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
        # Removido: self.atualizar_placeholder_chave_manual() daqui

    def atualizar_aba_manual(self, index):
        # Atualiza combo de pastas se a aba MANUAL estiver selecionada
        if self.tabs.tabText(index) == "MANUAL":
            self.manual_tab.atualizar_combo_pastas()
            self.atualizar_placeholder_chave_manual()  # Atualiza placeholder ao trocar de aba

    def selecionar_pasta(self):
        """Abre diálogo para selecionar pasta e preenche campo correspondente."""
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        # Corrigido: self.entrada_pasta não existe, então não faz nada aqui
        # Se necessário, implementar lógica para uso futuro
        pass

    def atualizar_placeholder_texto_entrada(self):
        """Atualiza o placeholder do campo de entrada conforme as categorias válidas."""
        categorias = self.input_categorias.text().strip()
        if categorias == "":
            self.texto_entrada.setPlaceholderText("chave: valor")
        else:
            self.texto_entrada.setPlaceholderText("chave.subchave: valor")

    def atualizar_placeholder_chave_manual(self):
        # Atualiza o placeholder do campo de chave da aba MANUAL
        categorias = self.input_categorias.text().strip()
        if hasattr(self, 'manual_tab'):
            if categorias == "":
                self.manual_tab.input_chave.setPlaceholderText("chave")
            else:
                self.manual_tab.input_chave.setPlaceholderText("chave.subchave")

    def processar_traducoes(self):
        """Inicia o processamento das traduções em thread separada."""
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
        # Filtrar linhas vazias
        entradas = [entrada.strip() for entrada in entradas if entrada.strip()]
        if not entradas:
            self.resultado_saida.setText("⚠️ Nenhum texto para processar. Digite algo no campo de entrada.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        # Verifica se categorias válidas está vazio
        categorias_validas = [cat.strip() for cat in self.input_categorias.text().strip().split(",") if cat.strip()]
        if not categorias_validas:
            # Permite formato chave: valor e insere na raiz
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
            # Chama a thread de tradução sem categorias válidas
            self.thread_traducao = TraducaoThread(entradas_formatadas, pasta_assets, usar_api, escrever_txt, atualizar_existente)
            self.thread_traducao.resultado_signal.connect(self.mostrar_resultado)
            self.thread_traducao.start()
        else:
            # Com categorias válidas, mantém o fluxo original
            self.thread_traducao = TraducaoThread(entradas, pasta_assets, usar_api, escrever_txt, atualizar_existente)
            self.thread_traducao.resultado_signal.connect(self.mostrar_resultado)
            self.thread_traducao.start()

    def ordenar_jsons(self):
        """Ordena os arquivos JSON por chave, mantendo a estrutura aninhada."""
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
        """Exibe o resultado do processamento na interface."""
        self.resultado_saida.setText(resultado)
        QTimer.singleShot(4000, lambda: self.resultado_saida.clear())

    def atualizar_config(self):
        """Atualiza o combo de pastas com as opções salvas."""
        self.combo_pastas.clear()
        for item in self.lista_caminhos:
            display_text = item['nome']
            self.combo_pastas.addItem(display_text, item['caminho'])

    def adicionar_pasta_config(self):
        """Adiciona uma nova pasta à lista de configurações."""
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if pasta and not any(item["caminho"] == pasta for item in self.lista_caminhos):
            nome, ok = QInputDialog.getText(self, "Nome da Pasta", "Digite um nome para essa pasta:")
            if ok and nome:
                novo = {"nome": nome, "caminho": pasta}
                self.lista_caminhos.append(novo)
                self.lista_widget.addItem(f"{nome}  →  {pasta}")
                # Não atualiza o combo da aba MANUAL aqui - só após salvar

    def remover_caminho(self):
        """Remove a pasta selecionada da lista de configurações."""
        row = self.lista_widget.currentRow()
        if row >= 0:
            self.lista_caminhos.pop(row)
            self.lista_widget.takeItem(row)
        self.atualizar_config()

    def guardar_config(self):
        """Salva as configurações de pastas e categorias no config.json."""
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
        # Atualiza o combo da aba MANUAL após salvar com sucesso
        if hasattr(self, 'manual_tab'):
            self.manual_tab.atualizar_combo_pastas()

    def carregar_caminhos_salvos(self):
        """Carrega as configurações salvas do config.json."""
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.lista_caminhos = dados.get("pastas", [])
                categorias = dados.get("categorias_validas", [])
                self.input_categorias.setText(", ".join(categorias))
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
        self.atualizar_config()


if __name__ == "__main__":
    app = QApplication([])
    icon_path = os.path.join(os.path.dirname(__file__), "rocket.ico")
    app.setWindowIcon(QIcon(icon_path))
    aplicar_tema_escuro(app)
    window = TradutorApp()
    window.show()
    app.exec()
