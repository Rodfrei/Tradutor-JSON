from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from components import criar_botao, criar_text_area
import tempfile
import os
import webbrowser

class HtmlTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Botão visualizar no topo ocupando 100% da largura
        self.btn_visualizar = criar_botao("Visualizar HTML", self.visualizar_html)
        layout.addWidget(self.btn_visualizar)
        
        # Textarea ocupando o resto da aba
        self.html_textarea = criar_text_area(
            placeholder="Digite seu código HTML aqui...",
            altura_minima=400
        )
        
        # Aplicar tema escuro explicitamente à textarea
        from PyQt6.QtGui import QPalette, QColor
        palette = self.html_textarea.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.html_textarea.setPalette(palette)
        
        layout.addWidget(self.html_textarea)
        
        self.setLayout(layout)
    
    def visualizar_html(self):
        """Cria um arquivo temporário com o HTML e abre no navegador padrão"""
        html_content = self.html_textarea.toPlainText().strip()
        
        if not html_content:
            return
        
        try:
            # Cria um arquivo temporário HTML
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(html_content)
                temp_file_path = temp_file.name
            
            # Abre o arquivo no navegador padrão
            webbrowser.open(f'file:///{temp_file_path.replace(os.sep, "/")}')
            
        except Exception as e:
            print(f"Erro ao visualizar HTML: {e}")