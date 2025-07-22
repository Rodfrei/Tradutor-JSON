import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import QTimer
from tradutor import carregar_json, salvar_json
from components import criar_botao, criar_label, criar_checkbox, criar_text_area, criar_combo_box


def get_nested(d, keys):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d


def set_nested(d, keys, value):
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


class ManualTab(QWidget):
    def __init__(self, pastas_callback):
        super().__init__()
        self.pastas_callback = pastas_callback
        self.fonte = None
        self.init_ui()

    def init_ui(self):
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
        layout = QVBoxLayout()
        self.fonte = QFont("Arial", 14)
        combo_layout = QHBoxLayout()
        self.combo_pastas = criar_combo_box(fonte=self.fonte)
        self.combo_pastas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.atualizar_combo_pastas()
        combo_layout.addWidget(self.combo_pastas)
        help_label = criar_label("?", largura_fixa=None)
        help_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        help_label.setStyleSheet("color: #42A2DA; cursor: pointer; padding: 5px;")
        help_label.setToolTip("""Inserção Direta de Traduções
• Digite a chave ou chave.subchave 
• Preencha os campos PT, EN, ES conforme necessário
• Marque os checkboxes dos idiomas obrigatórios
• Clique em "Traduzir" para inserir/atualizar as traduções
""")
        help_label.setStyleSheet("""
            QLabel {
                color: #42A2DA; 
                cursor: pointer; 
                padding: 5px;
            }
            QToolTip {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 8px;
                font-size: 11px;
                border-radius: 4px;
            }
        """)
        combo_layout.addWidget(help_label)
        layout.addLayout(combo_layout)
        label_width = 60
        linha_chave = QHBoxLayout()
        label_chave = criar_label("Chave:", fonte=self.fonte, largura_fixa=label_width)
        linha_chave.addWidget(label_chave)
        self.input_chave = QLineEdit()
        self.input_chave.setFont(self.fonte)
        self.input_chave.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_chave.setPlaceholderText("chave")
        linha_chave.addWidget(self.input_chave)
        layout.addLayout(linha_chave)
        linha_pt = QHBoxLayout()
        label_pt = criar_label("PT:", fonte=self.fonte, largura_fixa=label_width)
        linha_pt.addWidget(label_pt)
        self.input_pt = QLineEdit()
        self.input_pt.setFont(self.fonte)
        self.input_pt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        linha_pt.addWidget(self.input_pt)
        self.checkbox_pt = criar_checkbox(False, fonte=self.fonte)
        self.checkbox_pt.setToolTip("Obrigatório PT")
        linha_pt.addWidget(self.checkbox_pt)
        layout.addLayout(linha_pt)
        linha_en = QHBoxLayout()
        label_en = criar_label("EN:", fonte=self.fonte, largura_fixa=label_width)
        linha_en.addWidget(label_en)
        self.input_en = QLineEdit()
        self.input_en.setFont(self.fonte)
        self.input_en.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        linha_en.addWidget(self.input_en)
        self.checkbox_en = criar_checkbox(True, fonte=self.fonte)
        self.checkbox_en.setToolTip("Obrigatório EN")
        linha_en.addWidget(self.checkbox_en)
        layout.addLayout(linha_en)
        linha_es = QHBoxLayout()
        label_es = criar_label("ES:", fonte=self.fonte, largura_fixa=label_width)
        linha_es.addWidget(label_es)
        self.input_es = QLineEdit()
        self.input_es.setFont(self.fonte)
        self.input_es.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        linha_es.addWidget(self.input_es)
        self.checkbox_es = criar_checkbox(True, fonte=self.fonte)
        self.checkbox_es.setToolTip("Obrigatório ES")
        linha_es.addWidget(self.checkbox_es)
        layout.addLayout(linha_es)
        layout_botoes = QHBoxLayout()
        self.btn_adicionar = criar_botao("Traduzir", self.adicionar_traducao, fonte=self.fonte, altura_minima=32)
        layout_botoes.addWidget(self.btn_adicionar)
        self.btn_limpar = criar_botao("Limpar", self.limpar_campos, fonte=self.fonte, altura_minima=32)
        layout_botoes.addWidget(self.btn_limpar)
        layout.addLayout(layout_botoes)
        self.resultado_saida = criar_text_area(is_read_only=True, fonte=self.fonte, altura_fixa=80)
        layout.addWidget(self.resultado_saida)
        layout.addStretch()
        self.setLayout(layout)

    def atualizar_combo_pastas(self):
        self.combo_pastas.clear()
        pastas = self.pastas_callback() if callable(self.pastas_callback) else []
        if not isinstance(pastas, (list, tuple)):
            pastas = []
        for nome, caminho in pastas:
            self.combo_pastas.addItem(nome, caminho)

    def adicionar_traducao(self):
        chave = self.input_chave.text().strip()
        pt = self.input_pt.text().strip()
        en = self.input_en.text().strip()
        es = self.input_es.text().strip()
        pasta_assets = self.combo_pastas.currentData()
        obrig_pt = self.checkbox_pt.isChecked()
        obrig_en = self.checkbox_en.isChecked()
        obrig_es = self.checkbox_es.isChecked()
        if not pasta_assets:
            self.resultado_saida.setText("Selecione a pasta dos arquivos JSON.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        if not chave:
            self.resultado_saida.setText("Campo chave obrigatório.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        if obrig_pt and not pt:
            self.resultado_saida.setText("Campo PT obrigatório.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        if obrig_en and not en:
            self.resultado_saida.setText("Campo EN obrigatório.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        if obrig_es and not es:
            self.resultado_saida.setText("Campo ES obrigatório.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        caminho_pt = os.path.join(pasta_assets, "pt.json")
        caminho_en = os.path.join(pasta_assets, "en.json")
        caminho_es = os.path.join(pasta_assets, "es.json")
        pt_json = carregar_json(caminho_pt)
        en_json = carregar_json(caminho_en)
        es_json = carregar_json(caminho_es)
        keys = chave.split('.')
        existe_pt = get_nested(pt_json, keys) is not None
        if not existe_pt:
            if pt:
                set_nested(pt_json, keys, pt)
                salvar_json(caminho_pt, pt_json)
                self.resultado_saida.setText("✅ Chave criada no pt.json e traduções adicionadas!")
            else:
                self.resultado_saida.setText("❌ A chave não existe no pt.json e o campo PT está vazio.")
                QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
                return
        else:
            if pt:
                set_nested(pt_json, keys, pt)
                salvar_json(caminho_pt, pt_json)
        adicionado = False
        if obrig_en:
            set_nested(en_json, keys, en)
            adicionado = True
        if obrig_es:
            set_nested(es_json, keys, es)
            adicionado = True
        if not adicionado:
            self.resultado_saida.setText("Nada a adicionar.")
            QTimer.singleShot(4000, lambda: self.resultado_saida.clear())
            return
        salvar_json(caminho_en, en_json)
        salvar_json(caminho_es, es_json)
        if not existe_pt and pt:
            self.resultado_saida.setText("✅ Chave criada no pt.json e traduções adicionadas com sucesso!")
        else:
            self.resultado_saida.setText("✅ Tradução adicionada ou atualizada com sucesso!")
        QTimer.singleShot(4000, lambda: self.resultado_saida.clear())

    def limpar_campos(self):
        self.input_chave.clear()
        self.input_pt.clear()
        self.input_en.clear()
        self.input_es.clear() 