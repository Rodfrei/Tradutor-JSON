# Tradutor JSON

## Descrição

O **Tradutor JSON** é um software com interface gráfica que permite a tradução e gerenciamento de textos, organizando-os em arquivos JSON. Ele facilita a tradução de textos inseridos pelo usuário em diferentes idiomas.

A API utilizada para realizar a tradução é a **[MyMemory Translated](https://mymemory.translated.net/)**. Caso o uso da API esteja desativado, os textos são inseridos com sufixos EN e ES nos respectivos arquivos JSON.

---

## Interface Gráfica

- **Seleção de Pasta**: Permite ao usuário escolher a pasta que contém ou armazenará os arquivos de tradução.
- **Campo de Entrada de Textos**: Espaço onde o usuário insere os dados no formato `chave.subchave: valor`.
- Cada linha no campo entrada é considerado um item a ser inserido.
- **Configurações**:
  - **Uso da API**: Caixa de seleção para ativar ou desativar a tradução via API.
  - **Escrita no TXT**: Opção para salvar o histórico de labels inseridas.
- **Botões**:
  - **Processar Traduções**: Executa as traduções com base nos textos inseridos e configurações selecionadas.
- **Área de Resultados**: Exibe os resultados das traduções ou mensagens de erro diretamente na interface.

---

