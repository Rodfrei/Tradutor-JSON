# Tradutor JSON

## Descrição

O **Tradutor JSON** é um software com interface gráfica que permite a tradução e gerenciamento de textos, organizando-os em arquivos JSON. Ele facilita a tradução de textos inseridos pelo usuário em diferentes idiomas.

A API utilizada para realizar a tradução é a **[MyMemory Translated](https://mymemory.translated.net/)**. Caso o uso da API esteja desativado, os textos são inseridos com sufixos EN e ES nos respectivos arquivos JSON.

---

## Interface Gráfica

- **Seleção de Pasta**: Permite ao usuário escolher a pasta que contém ou armazenará os arquivos de tradução.
- **Campo de Entrada de Textos**: Espaço onde o usuário insere os dados no formato `chave.subchave: valor`.
- **Configurações**:
  - **Uso da API**: Caixa de seleção para ativar ou desativar a tradução via API.
  - **Escrita no TXT**: Opção para salvar o histórico de labels inseridas `.txt`.
- **Botões**:
  - **Processar Traduções**: Executa as traduções com base nos textos inseridos e configurações selecionadas.
- **Área de Resultados**: Exibe os resultados das traduções ou mensagens de erro diretamente na interface.

---

## API de Tradução

A aplicação utiliza a API **[MyMemory Translated](https://mymemory.translated.net/)** para traduzir textos do português para outros idiomas, como inglês e espanhol. A tradução é inserida de forma organizada em arquivos `.json`, podendo também ser escrita em um arquivo `.txt` caso configurado.

