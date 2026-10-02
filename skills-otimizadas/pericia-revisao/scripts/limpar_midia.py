# -*- coding: utf-8 -*-
"""Remove do .docx as imagens órfãs herdadas do precedente (técnica clear-and-rebuild).
Uso: python3 limpar_midia.py <arquivo.docx>            -> só relata
     python3 limpar_midia.py <arquivo.docx> --limpar   -> reescreve o arquivo sem as órfãs

Para cada parte (document.xml, headers, footers) cruza os ids r:embed/r:link/r:id realmente
usados com o respectivo arquivo .rels; relações de imagem não usadas são removidas, e arquivos de
word/media/ que nenhuma relação restante aponta são apagados do pacote. Fontes embutidas
(word/fonts/*.odttf) não são tocadas: são genéricas e não vazam dado de terceiro."""
import posixpath
import re
import shutil
import sys
import tempfile
import zipfile

IMG = "relationships/image"
RX_USO = re.compile(r'r:(?:embed|link|id)="([^"]+)"')
RX_REL = re.compile(r'<Relationship\b[^>]*/>')


def atributo(tag, nome):
    m = re.search(nome + r'="([^"]*)"', tag)
    return m.group(1) if m else ""


def analisar(z):
    nomes = set(z.namelist())
    novos_rels, remover_rels = {}, []
    for rels in [n for n in nomes if n.startswith("word/_rels/") and n.endswith(".rels")]:
        parte = "word/" + posixpath.basename(rels)[:-5]
        if parte not in nomes:
            continue
        usados = set(RX_USO.findall(z.read(parte).decode("utf-8")))
        xml = z.read(rels).decode("utf-8")
        orfas = [t for t in RX_REL.findall(xml)
                 if atributo(t, "Type").endswith(IMG) and atributo(t, "Id") not in usados
                 and atributo(t, "TargetMode") != "External"]
        if orfas:
            for t in orfas:
                xml = xml.replace(t, "")
                remover_rels.append((parte, atributo(t, "Id"), atributo(t, "Target")))
            novos_rels[rels] = xml.encode("utf-8")
    # mídia ainda apontada por alguma relação (após a remoção)
    apontadas = set()
    for rels in [n for n in nomes if n.endswith(".rels")]:
        xml = novos_rels.get(rels, z.read(rels)).decode("utf-8")
        base = posixpath.dirname(posixpath.dirname(rels))
        for t in RX_REL.findall(xml):
            alvo = atributo(t, "Target")
            if atributo(t, "TargetMode") != "External" and alvo:
                apontadas.add(posixpath.normpath(posixpath.join(base, alvo)).lstrip("/"))
    midia_orfa = sorted(n for n in nomes if n.startswith("word/media/") and n not in apontadas)
    return novos_rels, remover_rels, midia_orfa


def relatar(caminho):
    with zipfile.ZipFile(caminho) as z:
        _, rels, midia = analisar(z)
    return rels, midia


def limpar(caminho):
    with zipfile.ZipFile(caminho) as z:
        novos_rels, rels, midia = analisar(z)
        if not rels and not midia:
            return rels, midia
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
            for item in z.infolist():
                if item.filename in midia:
                    continue
                dados = novos_rels.get(item.filename, z.read(item.filename))
                out.writestr(item, dados)
    shutil.move(tmp, caminho)
    return rels, midia


if __name__ == "__main__":
    arq = sys.argv[1]
    rels, midia = limpar(arq) if "--limpar" in sys.argv else relatar(arq)
    if not rels and not midia:
        print("MÍDIA: nenhuma imagem órfã no pacote")
    else:
        acao = "removidas" if "--limpar" in sys.argv else "encontradas (rodar com --limpar)"
        print(f"MÍDIA: {len(rels)} relação(ões) e {len(midia)} arquivo(s) órfão(s) {acao}")
        for m in midia:
            print("  " + m)
