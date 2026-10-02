# -*- coding: utf-8 -*-
"""Checagem mecânica anti-IA de peças periciais.
Uso: python3 checar.py <arquivo.txt|arquivo.docx>
Imprime só as ocorrências encontradas (com número do parágrafo e trecho). Sem ocorrências:
imprime 'CHECAGEM MECÂNICA: APROVADO'."""
import re
import sys

PROIBIDAS = [
    "o laudo registrou que", "(grifo meu)", "unilateral", "não vincula o perito",
    "não vinculam o perito", "lotação formal não é determinante", "não está adstrita à inicial",
    "não está adstrita à narrativa", "ônus da prova recai", "obrigação legal da empregadora",
    "conforme evidenciado em oitivas", "nas oitivas colhidas", "vide corpo do laudo",
]
JARGAO = [
    "em suma", "em síntese", "à luz de", "destarte", "outrossim", "imperioso", "frisa-se",
    "cabalmente", "mister", "resta claro", "importante destacar", "cumpre salientar",
    "cumpre destacar", "nesse diapasão", "de igual modo", "corrobora",
]
REGEX = [
    ("travessão em-dash", re.compile("—")),
    ("empregado/obreiro (usar Reclamante)", re.compile(r"\b(empregad[oa]s?|obreir[oa]s?)\b", re.I)),
    ("reclamante minúsculo", re.compile(r"\breclamante\b")),
    ("NR com hífen (permitido só em citação)", re.compile(r"\bNR-\s?\d")),
    ("Sr./Sra. minúsculo", re.compile(r"(?<![A-Za-zÀ-ú])sra?\.\s", re.U)),
    ("aspas curvas (conferir se é citação permitida)", re.compile("[“”]")),
    ("placeholder", re.compile(r"\[(?!a confirmar)[^\]]{1,40}\]", re.I)),
    ("Markdown", re.compile(r"(\*\*|^#{1,6}\s|^\s*[-*]\s)", re.M)),
    ("pontuação duplicada", re.compile(r"(?<!\.)\.\.(?!\.)|,,|;;")),
    ("sessão (conferir: cessação?)", re.compile(r"\bsess(ão|ões)\b", re.I)),
]


def ler(caminho):
    if caminho.lower().endswith(".docx"):
        from docx import Document
        return [p.text for p in Document(caminho).paragraphs]
    with open(caminho, encoding="utf-8") as f:
        return f.read().split("\n")


def trecho(texto, ini, fim, margem=40):
    return "..." + texto[max(0, ini - margem):fim + margem].replace("\n", " ") + "..."


def checar_fontes(caminho):
    """No .docx: Verdana é o padrão; Arial só em enunciado de quesito; Tahoma só em cabeçalho e
    rodapé (que não entram aqui). Fonte herdada do estilo (None) é aceita."""
    from docx import Document
    achados = []
    for n, p in enumerate(Document(caminho).paragraphs, 1):
        for r in p.runs:
            fonte = r.font.name
            if not r.text.strip() or fonte in (None, "Verdana"):
                continue
            if fonte == "Arial":
                if "Resposta:" in r.text or p.text.strip().startswith("Resposta:"):
                    achados.append((n, "Resposta: deve ser Verdana, não Arial", trecho(r.text, 0, 60)))
                continue
            achados.append((n, f"fonte {fonte} (padrão é Verdana; Arial só em quesito)", trecho(r.text, 0, 60)))
    return achados


def main(caminho):
    pars = ler(caminho)
    achados = checar_fontes(caminho) if caminho.lower().endswith(".docx") else []
    for n, p in enumerate(pars, 1):
        baixo = p.lower()
        for termo in PROIBIDAS:
            i = baixo.find(termo)
            if i >= 0:
                achados.append((n, "frase proibida: " + termo, trecho(p, i, i + len(termo))))
        for termo in JARGAO:
            for m in re.finditer(r"\b" + re.escape(termo) + r"\b", baixo):
                achados.append((n, "jargão de IA: " + termo, trecho(p, m.start(), m.end())))
        for nome, rx in REGEX:
            for m in rx.finditer(p):
                achados.append((n, nome, trecho(p, m.start(), m.end())))
        if "contato permanente" in baixo and re.search(r"anexo\s*(n\.?º\s*)?(1|3|9|11|12|13)\b", baixo):
            achados.append((n, "contato permanente perto de Anexo diferente do 14", trecho(p, 0, 80)))
    if not achados:
        print("CHECAGEM MECÂNICA: APROVADO")
        return
    print(f"CHECAGEM MECÂNICA: {len(achados)} ocorrência(s)")
    for n, nome, t in achados:
        print(f"§{n} | {nome} | {t}")


if __name__ == "__main__":
    main(sys.argv[1])
