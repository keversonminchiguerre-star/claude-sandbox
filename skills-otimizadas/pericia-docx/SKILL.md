---
name: pericia-docx
description: Gera o arquivo DOCX de Laudo, Esclarecimentos ou Manifestação no molde aprovado de Keverson (estilos herdados do laudo mais recente). Usar uma vez, no fim, com o texto já aprovado, quando Keverson pedir para gerar o Word, montar o arquivo ou preparar para juntada.
---

# Geração de DOCX no Molde Aprovado

Usar com o texto já aprovado. Ajustes de texto se fazem antes, em texto; não regerar o DOCX a
cada ajuste. O texto aprovado é imutável: regenerar não altera texto validado.

## Princípio

Nunca reconstruir a formatação de memória. Conteúdo com python-docx; estilos (word/styles.xml,
word/theme/theme1.xml, word/fontTable.xml) transplantados do laudo mais recente do acervo (hoje o
169, pasta Laudo Técnico Pericial) por cirurgia de zip. Método aprovado em 07/06/2026 após três
reconstruções manuais falharem.

## Impressão digital do molde (169)

Corpo Verdana 12 justificado, espaçamento herdado do docDefaults (276), sem espaçamento direto.
Separação entre blocos por linhas em branco, nunca por espaço de parágrafo. Títulos em negrito,
justificados. Subtítulo adjacente ao título sem linha em branco. Cabeçalho, rodapé e contatos já
estão no `scripts/gerar_base.py`. Quesitos no formato do pericia-nucleo (função Q). Conclusão sem
negrito, destaque em caixa alta. Assinatura: Rio de Janeiro, [data]. + nome centralizado sem
negrito + Perito do Juízo. Dados bancários em bloco de linhas à esquerda.

## Imagens

Fotos vão dentro do DOCX, no Registro Fotográfico, centralizadas, 5.3 polegadas de largura; a
Lista de Presença logo abaixo do seu título. O pós-processamento comprime (máx. 1400 px, JPEG 78;
alvo abaixo de 2 MB com dez fotos).

## Procedimento

1. Gerar o conteúdo com `scripts/gerar_base.py` (helpers P, B, TIT, Q, FOTO; página A4 e
   margens já configuradas). Não ler os scripts: só importar e executar.
2. Rodar `scripts/posprocessar.py <gerado.docx> <laudo_referencia.docx>`.
3. Verificar por script (sem reler o documento no chat): nenhum "—" no corpo, sem aspas curvas no
   narrativo, NR sem hífen fora de citações, quesitos em Arial 11, contagem de [a confirmar].
   Reportar só o resultado.
4. Oferecer a revisão (pericia-revisao) em uma linha; só executar se Keverson pedir.

Scripts em /tmp somem quando o ambiente reinicia: os desta skill são a cópia permanente.
