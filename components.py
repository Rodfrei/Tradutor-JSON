from PyQt6.QtWidgets import QPushButton, QLabel, QTextEdit, QCheckBox, QComboBox, QListWidget
from PyQt6.QtGui import QFont


def criar_botao(texto, funcao=None, fonte=None, altura_minima=None):
    botao = QPushButton(texto)
    if fonte:
        botao.setFont(fonte)
    if funcao:
        botao.clicked.connect(funcao)
    if altura_minima:
        botao.setMinimumHeight(altura_minima)
    return botao


def criar_label(texto, fonte=None, largura_fixa=None):
    label = QLabel(texto)
    if fonte:
        label.setFont(fonte)
    if largura_fixa:
        label.setFixedWidth(largura_fixa)
    return label


def criar_text_area(is_read_only=False, fonte=None, placeholder=None, altura_minima=None, altura_fixa=None):
    text_area = QTextEdit()
    if fonte:
        text_area.setFont(fonte)
    text_area.setReadOnly(is_read_only)
    text_area.setAcceptRichText(False)
    if placeholder:
        text_area.setPlaceholderText(placeholder)
    if altura_minima:
        text_area.setMinimumHeight(altura_minima)
    if altura_fixa:
        text_area.setFixedHeight(altura_fixa)
    return text_area


def criar_checkbox(estado=False, texto="", fonte=None):
    checkbox = QCheckBox(texto)
    if fonte:
        checkbox.setFont(fonte)
    checkbox.setChecked(estado)
    return checkbox


def criar_combo_box(fonte=None):
    combo = QComboBox()
    if fonte:
        combo.setFont(fonte)
    return combo


def criar_lista_widget(fonte=None, altura_fixa=None):
    lista = QListWidget()
    if fonte:
        lista.setFont(fonte)
    if altura_fixa:
        lista.setFixedHeight(altura_fixa)
    return lista 