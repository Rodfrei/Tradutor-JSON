from PyQt6.QtWidgets import QPushButton, QLabel, QTextEdit, QCheckBox, QComboBox, QListWidget, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import QTimer

FONTE_PADRAO = QFont("Arial", 14)


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


def criar_botao(texto, funcao=None, altura_minima=None):
    botao = QPushButton(texto)
    botao.setFont(FONTE_PADRAO)
    if funcao:
        botao.clicked.connect(funcao)
    if altura_minima:
        botao.setMinimumHeight(altura_minima)
    return botao


def criar_label(texto, fonte=None, largura_fixa=None):
    from PyQt6.QtWidgets import QLabel
    label = QLabel(texto)
    label.setFont(fonte or FONTE_PADRAO)
    if largura_fixa:
        label.setFixedWidth(largura_fixa)
    return label


def criar_text_area(is_read_only=False, placeholder=None, altura_minima=None, altura_fixa=None):
    from PyQt6.QtWidgets import QSizePolicy
    text_area = QTextEdit()
    text_area.setFont(FONTE_PADRAO)
    text_area.setReadOnly(is_read_only)
    text_area.setAcceptRichText(False)
    if placeholder:
        text_area.setPlaceholderText(placeholder)
    if altura_minima:
        text_area.setMinimumHeight(altura_minima)
    if altura_fixa:
        text_area.setFixedHeight(altura_fixa)
    else:
        text_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return text_area


def criar_checkbox(estado=False, texto="", tooltip=None):
    checkbox = QCheckBox(texto)
    checkbox.setFont(FONTE_PADRAO)
    checkbox.setChecked(estado)
    if tooltip:
        checkbox.setToolTip(tooltip)
    return checkbox


def criar_combo_box(altura_minima=30):
    combo = QComboBox()
    combo.setFont(FONTE_PADRAO)
    from PyQt6.QtWidgets import QSizePolicy
    combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    combo.setMinimumHeight(altura_minima)
    return combo


def criar_lista_widget(altura_fixa=None):
    lista = QListWidget()
    lista.setFont(FONTE_PADRAO)
    if altura_fixa:
        lista.setFixedHeight(altura_fixa)
    return lista


def criar_line_edit(placeholder=None, expanding=True):
    line_edit = QLineEdit()
    line_edit.setFont(FONTE_PADRAO)
    if placeholder:
        line_edit.setPlaceholderText(placeholder)
    if expanding:
        from PyQt6.QtWidgets import QSizePolicy
        line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return line_edit


def criar_help_label(tooltip_text, texto_label="?"):
    help_label = QLabel(texto_label)
    help_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    help_label.setStyleSheet("color: #42A2DA; cursor: pointer; padding: 5px;")
    help_label.setToolTip(tooltip_text)
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
    return help_label 


def criar_hbox_layout(widgets):
    layout = QHBoxLayout()
    for widget in widgets:
        layout.addWidget(widget)
    return layout 


def limpar_widget_apos(widget, tempo_ms=4000, texto=None):
    if texto is not None and hasattr(widget, 'setText'):
        widget.setText(texto)
    def limpar():
        if hasattr(widget, 'clear'):
            widget.clear()
    QTimer.singleShot(tempo_ms, limpar) 