import json
import os
import requests

def carregar_categorias_validas():
    caminho_config = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(caminho_config):
        try:
            with open(caminho_config, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, dict):
                    return set(dados.get("categorias_validas", []))
        except Exception:
            pass
    return {"utils", "tooltip", "titulo", "menu", "mensagem", "label", "backend"}

CATEGORIAS_VALIDAS = carregar_categorias_validas()

def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        salvar_json(caminho, {})
        return {}

def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False, sort_keys=True)

def traduzir_texto(texto, destino):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": texto, "langpair": f"pt|{destino}"}
    try:
        response = requests.get(url, params=params).json()
        if "responseData" in response and response["responseData"]["translatedText"]:
            return response["responseData"]["translatedText"]
        else:
            return None
    except Exception:
        return None

def verificar_existencia(dados_json, niveis):
    ref = dados_json
    for nivel in niveis[:-1]:
        if nivel not in ref:
            return False
        ref = ref[nivel]
    return niveis[-1] in ref

def inserir_traducao(textos, pasta_assets, usar_api, escrever_txt, atualizar_existente=False, categorias_validas=None):

    if categorias_validas is None:
        categorias_validas = carregar_categorias_validas()

    caminho_pt = os.path.join(pasta_assets, "pt.json")
    caminho_en = os.path.join(pasta_assets, "en.json")
    caminho_es = os.path.join(pasta_assets, "es.json")
    caminho_txt = os.path.join(os.getcwd(), "traduzir.txt")

    pt_json = carregar_json(caminho_pt)
    en_json = carregar_json(caminho_en)
    es_json = carregar_json(caminho_es)

    for texto in textos:
        if ":" not in texto or "." not in texto:
            return f"==> Chave e subchave no formato inválido: '{texto.strip()}'"

        chave_completa, valor = texto.split(":", 1)
        chave_completa = chave_completa.strip()
        niveis = chave_completa.split(".")

        if niveis[0] not in categorias_validas:
            return f"==> Chave '{niveis[0]}' inválida"

        if verificar_existencia(pt_json, niveis) and not atualizar_existente:
            return f"==> A chave '{chave_completa}' já existe no JSON. Verifique!"

    with open(caminho_txt, "a", encoding="utf-8") as f:
        for texto in textos:
            texto = texto.strip()
            chave_completa, valor = texto.split(":", 1)
            chave_completa = chave_completa.strip()
            valor = valor.strip()
            niveis = chave_completa.split(".")

            def inserir_no_json(dados_json, niveis, valor):
                ref = dados_json
                for nivel in niveis[:-1]:
                    if nivel not in ref:
                        ref[nivel] = {}
                    ref = ref[nivel]
                if atualizar_existente or niveis[-1] not in ref:
                    ref[niveis[-1]] = valor

            if usar_api:
                traduzido_en = traduzir_texto(valor, "en")
                traduzido_es = traduzir_texto(valor, "es")
                if traduzido_en is None or traduzido_es is None:
                    return "==> Erro na API de tradução."
            else:
                traduzido_en = valor + " EN"
                traduzido_es = valor + " ES"

            inserir_no_json(pt_json, niveis, valor)
            inserir_no_json(en_json, niveis, traduzido_en)
            inserir_no_json(es_json, niveis, traduzido_es)

            if escrever_txt:
                if os.path.exists(caminho_txt):
                    with open(caminho_txt, "r", encoding="utf-8") as arquivo_txt:
                        linhas_existentes = arquivo_txt.readlines()
                else:
                    linhas_existentes = []

                chave_prefixo = f"{chave_completa}:"
                linhas_filtradas = [linha for linha in linhas_existentes if not linha.startswith(chave_prefixo)]

                linhas_filtradas.append(f"{chave_completa}: {valor}\n")

                with open(caminho_txt, "w", encoding="utf-8") as f:
                    f.writelines(linhas_filtradas)

    salvar_json(caminho_pt, pt_json)
    salvar_json(caminho_en, en_json)
    salvar_json(caminho_es, es_json)

    return "Todas as traduções foram inseridas com sucesso!"
