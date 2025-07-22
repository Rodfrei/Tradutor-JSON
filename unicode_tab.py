import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from components import criar_botao, criar_label, criar_text_area


class UnicodeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.fonte = None
        self.init_ui()

    def init_ui(self):
        from PyQt6.QtWidgets import QSizePolicy
        layout = QVBoxLayout()
        self.fonte = QFont("Arial", 14)
        label_entrada = criar_label("Texto de Entrada (Unicode to Escaped unicode sequence):", fonte=self.fonte)
        layout.addWidget(label_entrada)
        self.texto_entrada = criar_text_area(is_read_only=False, fonte=self.fonte, placeholder="Digite o texto aqui...", altura_minima=200)
        layout.addWidget(self.texto_entrada)
        layout_botoes = QHBoxLayout()
        self.btn_converter = criar_botao("Converter", self.converter_para_unicode, fonte=self.fonte, altura_minima=32)
        layout_botoes.addWidget(self.btn_converter)
        self.btn_limpar = criar_botao("Limpar", self.limpar_campos, fonte=self.fonte, altura_minima=32)
        layout_botoes.addWidget(self.btn_limpar)
        layout.addLayout(layout_botoes)
        label_saida = criar_label("Texto Convertido:", fonte=self.fonte)
        layout.addWidget(label_saida)
        self.texto_saida = criar_text_area(is_read_only=True, fonte=self.fonte, altura_minima=200)
        layout.addWidget(self.texto_saida)
        layout.addStretch()
        self.setLayout(layout)

    def converter_para_unicode(self):
        texto_entrada = self.texto_entrada.toPlainText().strip()
        if not texto_entrada:
            self.texto_saida.setText("⚠️ Digite algum texto para converter.")
            QTimer.singleShot(3000, lambda: self.texto_saida.clear())
            return
        try:
            texto_unicode = self._codificar_unicode(texto_entrada)
            self.texto_saida.setText(texto_unicode)
        except Exception as e:
            self.texto_saida.setText(f"❌ Erro na conversão: {e}")
            QTimer.singleShot(3000, lambda: self.texto_saida.clear())

    def _codificar_unicode(self, texto):
        try:
            resultado = ""
            for char in texto:
                if ord(char) < 128:
                    resultado += char
                else:
                    unicode_hex = hex(ord(char))[2:].upper().zfill(4)
                    resultado += f"\\u{unicode_hex}"
            return resultado
        except Exception as e:
            raise Exception(f"Erro ao codificar texto: {e}")

    def limpar_campos(self):
        self.texto_entrada.clear()
        self.texto_saida.clear() 