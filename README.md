Tradutor JSON 📝🌍
Descrição
Esta aplicação permite adicionar traduções a arquivos JSON de forma automática. Você pode escolher entre:
✅ Usar uma API de tradução ou adicionar traduções básicas automaticamente.
✅ Salvar as chaves inseridas em um arquivo traduzir.txt para controle.

Como Usar?
1️⃣ Abrir o programa (executável ou via Python).
2️⃣ Selecionar a pasta onde estão os arquivos JSON (pt.json, en.json, es.json).
3️⃣ Inserir os textos no formato:

less
Copiar
Editar
chave.subchave: Valor em português
4️⃣ Escolher as opções:

"Utilizar API de tradução" → Usa uma API para traduzir os textos.
"Escrever chaves em .txt" → Salva as chaves no traduzir.txt.
5️⃣ Clicar em "Processar Traduções" 🚀
Saída esperada
📂 No diretório selecionado:

Os arquivos pt.json, en.json e es.json serão atualizados.
O arquivo traduzir.txt (na raiz do projeto) terá as chaves adicionadas.
Gerando o Executável
Para criar um .exe, execute:

bash
Copiar
Editar
pyinstaller --onefile --windowed --icon=rocket.ico main.py
O executável estará na pasta dist/.

Requisitos
Python 3.x
PyQt6
Requests
bash
Copiar
Editar
pip install pyqt6 requests pyinstaller
