# -*- coding: utf-8 -*-
"""Confere, palavra por palavra, os enunciados de quesitos transcritos no .docx contra a peça
original da parte (PDF com texto ou .txt extraído).
Uso: python3 conferir_quesitos.py <laudo_ou_esclarecimentos.docx> <quesitos_parte.pdf|txt> [...]

Enunciados = parágrafos do .docx cujo texto está em Arial (padrão do molde). Para cada um, acha o
trecho mais parecido na(s) peça(s) e lista palavras trocadas, cortadas ou acrescentadas.
Diferença só de maiúscula/minúscula em "reclamante/Reclamante" é tolerada (convenção de Keverson);
qualquer outra diferença, inclusive de concordância de gênero ou pontuação final, é apontada."""
import difflib
import re
import sys

from docx import Document


def texto_fonte(caminho):
    if caminho.lower().endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(caminho) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        except ImportError:
            import subprocess
            return subprocess.run(["pdftotext", "-layout", caminho, "-"], capture_output=True,
                                  text=True, check=True).stdout
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def palavras(t):
    return re.findall(r"\w+|[^\w\s]", t, re.U)


def norm(p):
    return "reclamante" if p.lower() == "reclamante" else p


def enunciados(docx):
    out = []
    for n, p in enumerate(Document(docx).paragraphs, 1):
        runs = [r for r in p.runs if r.text.strip()]
        if runs and all(r.font.name == "Arial" for r in runs):
            out.append((n, p.text.strip()))
    return out


def melhor_trecho(alvo, fonte):
    k = len(alvo)
    melhor, inicio = 0.0, 0
    alvo_n = [norm(w).lower() for w in alvo]
    fonte_n = [norm(w).lower() for w in fonte]
    # janela deslizante com âncora na primeira palavra para ficar rápido
    candidatos = [i for i, w in enumerate(fonte_n) if alvo_n and w == alvo_n[0]] or range(len(fonte_n))
    for i in candidatos:
        r = difflib.SequenceMatcher(None, alvo_n, fonte_n[i:i + k + 5], autojunk=False).ratio()
        if r > melhor:
            melhor, inicio = r, i
    return melhor, fonte[inicio:inicio + k + 5]


def main(docx, fontes):
    fonte = palavras("\n".join(texto_fonte(f) for f in fontes))
    problemas = 0
    for n, enun in enunciados(docx):
        alvo = palavras(enun)
        score, trecho = melhor_trecho(alvo, fonte)
        a = [norm(w) for w in alvo]
        b = [norm(w) for w in trecho]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        difs = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            if op == "insert" and j1 >= len(a) + 0 and i1 == len(a):
                continue  # sobra do fim da janela
            difs.append(f"{op}: laudo [{' '.join(alvo[i1:i2])}] x original [{' '.join(trecho[j1:j2])}]")
        if score < 0.6:
            problemas += 1
            print(f"§{n} | NÃO LOCALIZADO na peça original (semelhança {score:.0%}) | {enun[:90]}")
        elif difs:
            problemas += 1
            print(f"§{n} | DIVERGE do original | {enun[:70]}")
            for d in difs:
                print("     " + d)
    print("CONFERÊNCIA DE QUESITOS: " + ("APROVADO" if not problemas else f"{problemas} enunciado(s) a corrigir"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
