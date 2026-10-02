# -*- coding: utf-8 -*-
"""Checagem mecânica anti-IA de peças periciais.
Uso: python3 checar.py <arquivo.txt|arquivo.docx>
Imprime só as ocorrências encontradas (com número do parágrafo e trecho). Sem ocorrências:
imprime 'CHECAGEM MECÂNICA: APROVADO'."""
import collections
import re
import sys

PROIBIDAS = [
    "o laudo registrou que", "unilateral", "não vincula o perito",
    "não vinculam o perito", "lotação formal não é determinante", "não está adstrita à inicial",
    "não está adstrita à narrativa", "ônus da prova recai", "obrigação legal da empregadora",
    "conforme evidenciado em oitivas", "nas oitivas colhidas", "vide corpo do laudo",
    "não aferível por meios periciais", "não aferíveis por meios periciais",
]
CONFERIR = [
    "não é possível apurar por meios periciais", "não foi possível a este perito",
    "não foi possível caracterizar", "não foi possível apurar",
]
JARGAO = [
    "em suma", "em síntese", "à luz de", "destarte", "outrossim", "imperioso", "frisa-se",
    "cabalmente", "mister", "resta claro", "importante destacar", "cumpre salientar",
    "cumpre destacar", "nesse diapasão", "de igual modo",
]
REGEX = [
    ("travessão em-dash", re.compile("—")),
    ("empregado/obreiro (usar Reclamante; exceção: cláusula fixa de Outras observações insalubridade)",
     re.compile(r"\b(empregad[oa]s?|obreir[oa]s?)\b", re.I)),
    ("RESPOSTA: em caixa alta (usar Resposta:)", re.compile(r"\bRESPOSTA:")),
    ("reclamante minúsculo", re.compile(r"\breclamante\b")),
    ("NR com hífen (permitido só em citação)", re.compile(r"\bNR-\s?\d")),
    ("Sr./Sra. minúsculo", re.compile(r"(?<![A-Za-zÀ-ú])sra?\.\s", re.U)),
    ("aspas curvas (conferir se é citação permitida)", re.compile("[“”]")),
    ("placeholder", re.compile(r"\[(?!a confirmar)[^\]]{1,40}\]", re.I)),
    ("Markdown", re.compile(r"(\*\*|^#{1,6}\s)", re.M)),
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


def checar_midia(caminho):
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from limpar_midia import relatar
    rels, midia = relatar(caminho)
    if not midia and not rels:
        return []
    return [(0, "imagem órfã de outro processo no pacote (rodar limpar_midia.py --limpar)",
             ", ".join(midia) or f"{len(rels)} relação(ões)")]


def checar_oj385(pars):
    texto = "\n".join(pars)
    if re.search(r"385", texto) and re.search(r"N[ÃA]O [ÉE] DEVIDO O ADICIONAL DE PERICULOSIDADE|"
                                              r"CARACTERIZA-SE", texto):
        return [(0, "OJ 385 citada com conclusão binária (deve ir ao Juízo, s.m.j.; conferir "
                    "se o tema é armazenamento em edifício vertical)", "")]
    return []


META = ["o texto deixa claro", "assim o texto", "o perito não adotou", "nota para mim",
        "deixa claro que o perito", "esta redação", "nesta reescrita"]


def checar_nomes(pars):
    """Mesma pessoa grafada de formas diferentes (ex.: Guedes x Gomes) após Sr./Sra."""
    rx = re.compile(r"\bSra?\.\s+((?:[A-ZÀ-Ý][a-zà-ÿ]+)(?:\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][a-zà-ÿ]+){0,5})")
    por_nome = collections.defaultdict(set)
    for p in pars:
        for m in rx.finditer(p):
            por_nome[m.group(1).split()[0]].add(m.group(1))
    achados = []
    for primeiro, variantes in por_nome.items():
        v = sorted(variantes, key=len)
        conflito = any(not (b.startswith(a) or a.startswith(b)) for a in v for b in v if a < b)
        if conflito:
            achados.append((0, f"nome com grafias diferentes no mesmo documento ({primeiro})", " | ".join(v)))
    return achados


def main(caminho):
    pars = ler(caminho)
    achados = checar_fontes(caminho) + checar_midia(caminho) if caminho.lower().endswith(".docx") else []
    achados += checar_oj385(pars) + checar_nomes(pars)
    for n, p in enumerate(pars, 1):
        if any(termo in p.lower() for termo in META):
            achados.append((n, "meta-comentário (não é texto de laudo)", trecho(p, 0, 80)))
    for n, p in enumerate(pars, 1):
        baixo = p.lower()
        for termo in PROIBIDAS:
            i = baixo.find(termo)
            if i >= 0:
                achados.append((n, "frase proibida: " + termo, trecho(p, i, i + len(termo))))
        for termo in CONFERIR:
            i = baixo.find(termo)
            if i >= 0:
                achados.append((n, "conferir impossibilidade: só vale se não houver NENHUM elemento "
                                   "sobre o ponto; havendo, usar 'os elementos apurados não evidenciam'",
                                trecho(p, i, i + len(termo))))
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
