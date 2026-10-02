# -*- coding: utf-8 -*-
"""Mede convenções de formatação no acervo real e mostra a frequência de cada variante.
Uso: python3 medir_acervo.py "<pasta Laudo Técnico Pericial>" [--min 150]
     --min N: considera só arquivos cujo nome começa com número >= N (laudos recentes).
Só lê; nunca altera arquivo do acervo.

Mede, por laudo: alinhamento dos títulos de seção; negrito e caixa alta do destaque da conclusão
("NÃO É DEVIDO...", "CARACTERIZA-SE..."); posição da lista de presença (imagem logo após
"Acompanharam a diligência" ou no Registro fotográfico) e se há legenda "Lista de Presença";
marcador nativo na lista de "Acompanharam"; "Resposta:" x "RESPOSTA:"; fonte dos títulos; negrito
dos títulos de quesitos; "(Grifo meu)" presente."""
import collections
import os
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

TITULOS = ["Objetivo", "Diligência Pericial", "Acompanharam a diligência", "Aspectos Laborais",
           "Metodologia", "Equipamentos de proteção individual", "Encerramento"]
ALIN = {WD_ALIGN_PARAGRAPH.JUSTIFY: "justificado", WD_ALIGN_PARAGRAPH.LEFT: "esquerda",
        WD_ALIGN_PARAGRAPH.CENTER: "centro", None: "herdado"}


def tem_imagem(p):
    return bool(p._p.xpath(".//pic:pic"))


def negrito(p):
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all(r.bold for r in runs)


def fonte(p):
    nomes = {r.font.name for r in p.runs if r.text.strip()}
    return "/".join(sorted(n or "herdada" for n in nomes)) or "-"


def medir(caminho, c):
    pars = Document(caminho).paragraphs
    textos = [p.text.strip() for p in pars]
    for p, t in zip(pars, textos):
        if t in TITULOS:
            c["título: alinhamento"][ALIN.get(p.alignment, str(p.alignment))] += 1
            c["título: fonte"][fonte(p)] += 1
        if re.match(r"^(NÃO|N[AÃ]O) [ÉE] DEVIDO|^CARACTERIZA-SE|^GRAU (MÉDIO|MÁXIMO)", t, re.I):
            c["destaque da conclusão: negrito"]["sim" if negrito(p) else "não"] += 1
            c["destaque da conclusão: caixa"]["ALTA" if t.isupper() else "mista"] += 1
        if t.startswith("RESPOSTA:"):
            c["resposta"]["RESPOSTA:"] += 1
        elif t.startswith("Resposta:"):
            c["resposta"]["Resposta:"] += 1
        if t.lower().startswith(("respostas aos quesitos", "quesitos do reclamante",
                                 "quesitos da reclamante", "quesitos da reclamada")):
            c["títulos de quesitos: negrito"]["sim" if negrito(p) else "não"] += 1
        if "(Grifo meu)" in t:
            c["(Grifo meu)"]["presente"] += 1
    # lista de presença
    try:
        i = next(k for k, t in enumerate(textos) if t.startswith("Acompanharam a diligência"))
    except StopIteration:
        return
    j = next((k for k in range(i + 1, len(textos)) if textos[k].startswith("Aspectos Laborais")),
             len(textos))
    trecho = pars[i + 1:j]
    c["lista de presença: imagem após Acompanharam"]["sim" if any(map(tem_imagem, trecho)) else "não"] += 1
    c["lista de presença: legenda/título no trecho"][
        "sim" if any(p.text.strip().lower() == "lista de presença" for p in trecho) else "não"] += 1
    itens = [p for p in trecho if p.text.strip() and not tem_imagem(p)
             and p.text.strip().lower() != "lista de presença"]
    if itens:
        c["Acompanharam: marcador nativo"][
            "sim" if all(p._p.pPr is not None and p._p.pPr.numPr is not None for p in itens) else "não"] += 1
        sep = "–" if any("–" in p.text for p in itens) else "-" if any(" - " in p.text for p in itens) else "outro"
        c["Acompanharam: separador nome/cargo"][sep] += 1
    k = next((k for k, t in enumerate(textos) if t.lower().startswith("registro fotográfico")), None)
    if k is not None:
        c["lista de presença: legenda no Registro fotográfico"][
            "sim" if any(t.lower().startswith("lista de presença") for t in textos[k:]) else "não"] += 1


def main(pasta, minimo):
    arquivos = []
    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith(".docx") or "esclarec" in nome.lower() or "manifest" in nome.lower():
            continue
        m = re.match(r"(\d+)", nome)
        if minimo and (not m or int(m.group(1)) < minimo):
            continue
        arquivos.append(nome)
    c = collections.defaultdict(collections.Counter)
    for nome in arquivos:
        try:
            medir(os.path.join(pasta, nome), c)
        except Exception as e:  # arquivo corrompido ou bloqueado: segue
            print(f"(ignorado {nome}: {e})")
    print(f"LAUDOS MEDIDOS: {len(arquivos)}")
    for chave in sorted(c):
        total = sum(c[chave].values())
        partes = ", ".join(f"{v}: {n} ({n * 100 // total}%)" for v, n in c[chave].most_common())
        print(f"{chave}: {partes}")


if __name__ == "__main__":
    minimo = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0
    main(sys.argv[1], minimo)
