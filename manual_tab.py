import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import QTimer
from tradutor import carregar_json, salvar_json
from components import criar_botao, criar_label, criar_checkbox, criar_text_area, criar_combo_box, criar_line_edit, criar_help_label, criar_hbox_layout, limpar_widget_apos


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
    def __init__(self, pastas_callback, input_categorias):
        super().__init__()
        self.pastas_callback = pastas_callback
        self.input_categorias = input_categorias
        self.init_ui()

    def init_ui(self):
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
        layout = QVBoxLayout()
        self.fonte = QFont("Arial", 14)
        self.combo_pastas = criar_combo_box(fonte=self.fonte)
        self.atualizar_combo_pastas()
        combo_layout = criar_hbox_layout([
            self.combo_pastas,
            criar_help_label("""Inserção Direta de Traduções\n• Digite a chave ou chave.subchave \n• Preencha os campos PT, EN, ES conforme necessário\n• Ao desmarcar um checkbox, a tradução não é adicionada\n• Clique em \"Traduzir\" para inserir/atualizar as traduções\n""")
        ])
        label_width = 60
        linha_chave = criar_hbox_layout([
            criar_label("Chave:", fonte=self.fonte, largura_fixa=label_width),
            criar_line_edit(fonte=self.fonte, placeholder="chave", expanding=True)
        ])
        self.input_chave = linha_chave.itemAt(1).widget()
        linha_pt = criar_hbox_layout([
            criar_label("PT:", fonte=self.fonte, largura_fixa=label_width),
            criar_line_edit(fonte=self.fonte, expanding=True)
        ])
        self.input_pt = linha_pt.itemAt(1).widget()
        linha_en = criar_hbox_layout([
            criar_label("EN:", fonte=self.fonte, largura_fixa=label_width),
            criar_line_edit(fonte=self.fonte, expanding=True),
            criar_checkbox(True, texto=" ", fonte=self.fonte)
        ])
        self.input_en = linha_en.itemAt(1).widget()
        self.checkbox_en = linha_en.itemAt(2).widget()
        linha_es = criar_hbox_layout([
            criar_label("ES:", fonte=self.fonte, largura_fixa=label_width),
            criar_line_edit(fonte=self.fonte, expanding=True),
            criar_checkbox(True, texto=" ", fonte=self.fonte)
        ])
        self.input_es = linha_es.itemAt(1).widget()
        self.checkbox_es = linha_es.itemAt(2).widget()
        self.btn_adicionar = criar_botao("Traduzir", self.adicionar_traducao, fonte=self.fonte, altura_minima=32)
        self.btn_limpar = criar_botao("Limpar", self.limpar_campos, fonte=self.fonte, altura_minima=32)
        layout_botoes = criar_hbox_layout([
            self.btn_adicionar,
            self.btn_limpar
        ])
        self.resultado_saida = criar_text_area(is_read_only=True, fonte=self.fonte)
        widgets = [
            combo_layout,
            linha_chave,
            linha_pt,
            linha_en,
            linha_es,
            layout_botoes,
            self.resultado_saida
        ]
        for item in widgets:
            if hasattr(item, 'addWidget') or hasattr(item, 'addLayout'):
                layout.addLayout(item)
            else:
                layout.addWidget(item)
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
        # Validação de categorias válidas igual à aba JSON
        categorias_validas = [cat.strip() for cat in self.input_categorias.text().strip().split(",") if cat.strip()]
        if categorias_validas:
            categoria_chave = chave.split('.')[0]
            if categoria_chave not in categorias_validas:
                limpar_widget_apos(self.resultado_saida, 4000, f"Chave '{categoria_chave}' inválida. Categorias válidas: {', '.join(sorted(categorias_validas))}")
                return
        pasta_assets = self.combo_pastas.currentData()
        obrig_en = self.checkbox_en.isChecked()
        obrig_es = self.checkbox_es.isChecked()
        caminho_pt = os.path.join(pasta_assets, "pt.json")
        caminho_en = os.path.join(pasta_assets, "en.json")
        caminho_es = os.path.join(pasta_assets, "es.json")
        pt_json = carregar_json(caminho_pt)
        en_json = carregar_json(caminho_en)
        es_json = carregar_json(caminho_es)
        keys = chave.split('.')
        existe_pt = get_nested(pt_json, keys) is not None
                
        if not pasta_assets:
            limpar_widget_apos(self.resultado_saida, 4000, "Selecione a pasta dos arquivos JSON.")
            return
        if not chave:
            limpar_widget_apos(self.resultado_saida, 4000, "Campo chave obrigatório.")
            return
        if not pt and not existe_pt:
            limpar_widget_apos(self.resultado_saida, 4000, "Campo PT obrigatório.")
            return
        if obrig_en and not en:
            limpar_widget_apos(self.resultado_saida, 4000, "Campo EN obrigatório.")
            return
        if obrig_es and not es:
            limpar_widget_apos(self.resultado_saida, 4000, "Campo ES obrigatório.")
            return

        if not existe_pt:
            if pt:
                set_nested(pt_json, keys, pt)
                salvar_json(caminho_pt, pt_json)
                self.resultado_saida.setText("Chave criada no pt.json e traduções adicionadas!")
            else:
                limpar_widget_apos(self.resultado_saida, 4000, "A chave não existe no pt.json e o campo PT está vazio.")
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
            limpar_widget_apos(self.resultado_saida, 4000, "Nada a adicionar.")
            return
        salvar_json(caminho_en, en_json)
        salvar_json(caminho_es, es_json)
        if not existe_pt and pt:
            limpar_widget_apos(self.resultado_saida, 4000, "Chave criada no pt.json e traduções adicionadas com sucesso!" if not existe_pt and pt else "Tradução adicionada ou atualizada com sucesso!")
        else:
            limpar_widget_apos(self.resultado_saida, 4000, "Tradução adicionada ou atualizada com sucesso!")

    def limpar_campos(self):
        self.input_chave.clear()
        self.input_pt.clear()
        self.input_en.clear()
        self.input_es.clear() 