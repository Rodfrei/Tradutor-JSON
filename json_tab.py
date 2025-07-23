import os
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from components import criar_combo_box, criar_text_area, criar_botao, criar_checkbox, criar_hbox_layout, limpar_widget_apos
from tradutor import inserir_traducao

class JsonTab(QWidget):
    def __init__(self, lista_caminhos, categorias_validas=None):
        super().__init__()
        self.lista_caminhos = lista_caminhos
        self.categorias_validas = categorias_validas or []
        layout_json = QVBoxLayout()
        self.combo_pastas = criar_combo_box()
        self.combo_pastas.setMinimumHeight(30)
        for item in self.lista_caminhos:
            self.combo_pastas.addItem(item['nome'], item['caminho'])
        self.texto_entrada = criar_text_area(
            False,
            placeholder=self._placeholder_texto_entrada()
        )
        self.resultado_saida = criar_text_area(True, altura_fixa=80)
        self.btn_processar = criar_botao("Processar", self.processar_traducoes)
        self.btn_ordenar = criar_botao("Ordenar", self.ordenar_jsons)
        self.checkbox_api = criar_checkbox(False, "Utilizar API")
        self.checkbox_atualizar = criar_checkbox(False, "Atualizar existentes")
        self.checkbox_txt = criar_checkbox(True, "Escrever em .txt")
        layout_botoes = criar_hbox_layout([self.btn_processar, self.btn_ordenar])
        layout_checks = criar_hbox_layout([self.checkbox_api, self.checkbox_atualizar, self.checkbox_txt])
        widgets = [
            self.combo_pastas, self.texto_entrada,
            layout_checks, layout_botoes, self.resultado_saida
        ]
        for widget in widgets:
            if hasattr(widget, 'addWidget') or hasattr(widget, 'addLayout'):
                layout_json.addLayout(widget)
            else:
                layout_json.addWidget(widget)
        self.setLayout(layout_json)

    def _placeholder_texto_entrada(self):
        if self.categorias_validas:
            return "chave.subchave: valor"
        return "chave: valor"

    def set_categorias_validas(self, categorias):
        categorias = categorias or []
        self.categorias_validas = categorias
        self.texto_entrada.setPlaceholderText(self._placeholder_texto_entrada())

    def processar_traducoes(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self._msg("Selecione uma pasta de arquivos JSON para continuar.")
            return
        entradas = [l.strip() for l in self.texto_entrada.toPlainText().split("\n") if l.strip()]
        if not entradas:
            self._msg("Nenhum texto para processar. Digite algo no campo de entrada.")
            return
        # Chamar a função de tradução real (validações feitas lá)
        resultado = inserir_traducao(
            entradas,
            pasta_assets,
            self.checkbox_api.isChecked(),
            self.checkbox_txt.isChecked(),
            self.checkbox_atualizar.isChecked(),
            categorias_validas=self.categorias_validas
        )
        self._msg(resultado)

    def ordenar_jsons(self):
        pasta_assets = self.combo_pastas.currentData()
        if not pasta_assets:
            self._msg("Selecione uma pasta de arquivos JSON para continuar.")
            return
        self.resultado_saida.setText("Ordenando arquivos JSON...")
        for lang in ["pt", "en", "es"]:
            caminho = os.path.join(pasta_assets, f"{lang}.json")
            if not os.path.exists(caminho):
                continue
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception as e:
                self._msg(f"Erro ao ler {lang}.json: {e}")
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
                self._msg(f"Erro ao salvar {lang}.json: {e}")
                continue
        self._msg("Arquivos JSON ordenados com sucesso!")

    def mostrar_resultado(self, resultado):
        self._msg(resultado)

    def _msg(self, texto):
        self.resultado_saida.setText(texto)
        limpar_widget_apos(self.resultado_saida, 4000) 