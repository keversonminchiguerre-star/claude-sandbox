# -*- coding: utf-8 -*-
"""Gera a Lista de Presença (xlsx) no molde das listas 73 e 90.
Uso: python3 lista_presenca.py proc.json "Lista de Presença - <processo>.xlsx"
ou: from lista_presenca import build_lista_presenca; build_lista_presenca(saida, proc)

Armadilhas já resolvidas aqui: não fixar altura em linha com wrap_text e texto longo (corta o
texto); fitToPage obrigatório para caber em uma página; rótulo longo com wrap e vertical top."""
import json
import re
import sys

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side

FONT_NAME = "Verdana"
THIN = Side(style="thin", color="000000")
BORDER_ALL = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def bold(size=10): return Font(name=FONT_NAME, size=size, bold=True)
def reg(size=10):  return Font(name=FONT_NAME, size=size, bold=False)


def separar_diligencia(texto):
    """'12/05/2026, às 10h00, na Rua X' -> ('12/05/2026', '10h00', 'Rua X')."""
    m = re.match(r'(\d{2}/\d{2}/\d{4}),\s*às\s*(\d{2}h\d{2}),\s*(.*)', texto)
    if not m:
        return None
    local = re.sub(r'^(nas?|nos?)\s+', '', m.group(3).strip())
    return m.group(1), m.group(2), local[:1].upper() + local[1:]


def build_lista_presenca(out_path, proc):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Planilha1"

    for col, w in [('A', 2.5), ('B', 9.14), ('C', 7.86), ('D', 27.14),
                   ('E', 15.14), ('F', 15.43), ('G', 8.71), ('H', 8.71)]:
        ws.column_dimensions[col].width = w

    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = 'portrait'
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.511811024
    ws.page_margins.top = ws.page_margins.bottom = 0.787401575

    r = 2

    def label_value(row, label, value, wrap=False, merge_label=False):
        label_wrap = len(label) > 13
        c = ws.cell(row=row, column=2, value=label); c.font = bold()
        c.alignment = Alignment(horizontal='left',
                                vertical='top' if (wrap or label_wrap) else None,
                                wrap_text=label_wrap)
        if merge_label:
            ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=3)
        v = ws.cell(row=row, column=4, value=value); v.font = bold()
        v.alignment = Alignment(horizontal='left',
                                vertical='top' if wrap else None, wrap_text=wrap)
        ws.merge_cells(start_row=row, start_column=4, end_row=row, end_column=8)
        return row + 1   # nunca fixar altura aqui

    r = label_value(r, "Processo:", proc["numero"])
    for lbl, val in proc["partes"]:
        r = label_value(r, lbl, val, wrap=len(val) > 60, merge_label=True)

    ws.row_dimensions[r].height = 9; r += 1
    ws.cell(row=r, column=2, value="Data:").font = bold()
    ws.cell(row=r, column=3, value=proc["data"]).font = bold()
    r += 1
    ws.row_dimensions[r].height = 9; r += 1

    c = ws.cell(row=r, column=2, value=f"Local da Perícia: {proc['local']}")
    c.font = bold(); c.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
    ws.row_dimensions[r].height = 30
    r += 1
    ws.row_dimensions[r].height = 9; r += 1

    ws.cell(row=r, column=2, value="Início:").font = bold()
    ws.cell(row=r, column=3, value=proc["hora_inicio"]).font = bold()
    ws.cell(row=r, column=5, value="Término:").font = bold()
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=8)
    r += 1
    ws.row_dimensions[r].height = 9; r += 1

    ws.cell(row=r, column=2, value="Compareceram:").font = bold()
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
    r += 1

    for sc, ec, text in [(2, 4, "Nome"), (5, 5, "Doc. Ident."), (6, 6, "Função/Parte"), (7, 8, "Assinatura")]:
        cell = ws.cell(row=r, column=sc, value=text)
        cell.font = bold(); cell.alignment = Alignment(horizontal='center', vertical='center')
        if ec > sc:
            ws.merge_cells(start_row=r, start_column=sc, end_row=r, end_column=ec)
        for col in range(sc, ec + 1):
            ws.cell(row=r, column=col).border = BORDER_ALL
    r += 1

    for i in range(12):
        row = r + i
        ws.row_dimensions[row].height = 23.25
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=4)
        ws.merge_cells(start_row=row, start_column=7, end_row=row, end_column=8)
        for col in range(2, 9):
            cell = ws.cell(row=row, column=col)
            cell.border = BORDER_ALL; cell.font = reg()
    r += 12

    ws.row_dimensions[r].height = 15.75; r += 1
    ws.cell(row=r, column=2, value="Observações:").font = bold()
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
    r += 1

    for i in range(4):
        row = r + i
        ws.row_dimensions[row].height = 18
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=8)
        for col in range(2, 9):
            ws.cell(row=row, column=col).border = Border(top=THIN, bottom=THIN)

    wb.save(out_path)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        build_lista_presenca(sys.argv[2], json.load(f))
