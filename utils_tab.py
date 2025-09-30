from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from components import criar_label, criar_botao, criar_text_area, criar_input_numero, criar_date_edit
import random
import requests
import json

class UtilsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
 
        self.ip_saida = criar_text_area(is_read_only=True, altura_fixa=40)
        self.ip_saida.setText("Clique em 'Obter IP' para verificar")
        btn_obter_ip = criar_botao("Obter IP", self.obter_ip_publico)
        layout.addWidget(btn_obter_ip)
        layout.addWidget(self.ip_saida)
        
        layout.addSpacing(20)
        
        layout.addWidget(criar_label("Gerador de CPF"))
        self.cpf_saida = criar_text_area(is_read_only=True, altura_fixa=40)
        btn_gerar_cpf = criar_botao("Gerar CPF", self.gerar_cpf)
        layout.addWidget(btn_gerar_cpf)
        layout.addWidget(self.cpf_saida)
  
        layout.addSpacing(20)
        layout.addWidget(criar_label("Somador/Subtrator de Data"))
        data_layout = QHBoxLayout()
        self.data_edit = criar_date_edit()
        self.input_dias = criar_input_numero(placeholder="Dias (+/-)")
        btn_calcular = criar_botao("Calcular", self.calcular_data)
        data_layout.addWidget(self.data_edit)
        data_layout.addWidget(self.input_dias)
        data_layout.addWidget(btn_calcular)
        layout.addLayout(data_layout)
        self.data_saida = criar_text_area(is_read_only=True, altura_fixa=40)
        layout.addWidget(self.data_saida)
        layout.addStretch()
        layout.addSpacing(20)
        self.lorem_area = criar_text_area(is_read_only=True, altura_fixa=80)
        self.lorem_area.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        layout.addWidget(self.lorem_area)
        self.setLayout(layout)

    def gerar_cpf(self):
        def calc_digito(digs):
            s = sum([(len(digs)+1-i)*int(num) for i, num in enumerate(digs)])
            r = 11 - s % 11
            return str(r if r < 10 else 0)
        n = [str(random.randint(0,9)) for _ in range(9)]
        n.append(calc_digito(n))
        n.append(calc_digito(n))
        cpf_num = ''.join(n)
        cpf_mask = f"{cpf_num[:3]}.{cpf_num[3:6]}.{cpf_num[6:9]}-{cpf_num[9:]}"
        self.cpf_saida.setText(cpf_mask)

    def calcular_data(self):
        try:
            dias = int(self.input_dias.text())
        except ValueError:
            self.data_saida.setText("Digite um número válido de dias.")
            return
        data = self.data_edit.date()
        nova_data = data.addDays(dias)
        self.data_saida.setText(nova_data.toString("dd/MM/yyyy"))
    
    def obter_ip_publico(self):
        try:
            self.ip_saida.setText("Verificando...")
            apis = [
                "https://httpbin.org/ip",
                "https://api.ipify.org?format=json",
                "https://jsonip.com"
            ]
            
            for api in apis:
                try:
                    response = requests.get(api, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if 'origin' in data:
                            ip = data['origin']
                        elif 'ip' in data:
                            ip = data['ip']
                        else:
                            continue
                        
                        self.ip_saida.setText(ip)
                        return
                except:
                    continue
            
            self.ip_saida.setText("Erro ao obter IP público")
            
        except Exception as e:
            self.ip_saida.setText("Erro de conexão") 