import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont


class UnicodeTab(QWidget):
    """Aba UNICODE para conversão de texto para sequências Unicode"""
    def __init__(self):
        super().__init__()
        self.fonte = None
        self.init_ui()

    def init_ui(self):
        from PyQt6.QtWidgets import QSizePolicy
        layout = QVBoxLayout()
        self.fonte = QFont("Arial", 14)

        # Campo de entrada
        label_entrada = QLabel("Texto de Entrada (Unicode to Escaped unicode sequence):")
        label_entrada.setFont(self.fonte)
        layout.addWidget(label_entrada)

        self.texto_entrada = QTextEdit()
        self.texto_entrada.setFont(self.fonte)
        self.texto_entrada.setPlaceholderText("Digite o texto aqui...")
        self.texto_entrada.setMinimumHeight(200)
        self.texto_entrada.setAcceptRichText(False)
        layout.addWidget(self.texto_entrada)

        # Botões
        layout_botoes = QHBoxLayout()
        
        self.btn_converter = QPushButton("Converter")
        self.btn_converter.setFont(self.fonte)
        self.btn_converter.clicked.connect(self.converter_para_unicode)
        self.btn_converter.setMinimumHeight(32)
        layout_botoes.addWidget(self.btn_converter)
        
        self.btn_limpar = QPushButton("Limpar")
        self.btn_limpar.setFont(self.fonte)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_limpar.setMinimumHeight(32)
        layout_botoes.addWidget(self.btn_limpar)
        
        layout.addLayout(layout_botoes)

        # Campo de saída
        label_saida = QLabel("Texto Convertido:")
        label_saida.setFont(self.fonte)
        layout.addWidget(label_saida)

        self.texto_saida = QTextEdit()
        self.texto_saida.setFont(self.fonte)
        self.texto_saida.setReadOnly(True)
        self.texto_saida.setMinimumHeight(200)
        self.texto_saida.setAcceptRichText(False)
        layout.addWidget(self.texto_saida)

        layout.addStretch()
        self.setLayout(layout)

    def converter_para_unicode(self):
        """Converte o texto de entrada para sequências Unicode."""
        texto_entrada = self.texto_entrada.toPlainText().strip()
        
        if not texto_entrada:
            self.texto_saida.setText("⚠️ Digite algum texto para converter.")
            QTimer.singleShot(3000, lambda: self.texto_saida.clear())
            return
        
        try:
            # Converter para Unicode
            texto_unicode = self._codificar_unicode(texto_entrada)
            self.texto_saida.setText(texto_unicode)
        except Exception as e:
            self.texto_saida.setText(f"❌ Erro na conversão: {e}")
            QTimer.singleShot(3000, lambda: self.texto_saida.clear())

    def _codificar_unicode(self, texto):
        """Codifica caracteres especiais para sequências Unicode."""
        try:
            resultado = ""
            for char in texto:
                # Se o caractere é ASCII (0-127), mantém como está
                if ord(char) < 128:
                    resultado += char
                else:
                    # Se é um caractere Unicode, converte para \uXXXX
                    unicode_hex = hex(ord(char))[2:].upper().zfill(4)
                    resultado += f"\\u{unicode_hex}"
            return resultado
        except Exception as e:
            raise Exception(f"Erro ao codificar texto: {e}")

    def limpar_campos(self):
        """Limpa os campos de entrada e saída."""
        self.texto_entrada.clear()
        self.texto_saida.clear() 