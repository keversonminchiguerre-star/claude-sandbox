---
name: pericia-pre-laudo
description: Montagem do Pré-Laudo a partir dos PDFs dos autos, antes da diligência - inventário da pasta, extração, aspectos laborais, sínteses, documentos evidenciados, EPI, metodologia e pendências. Usar quando Keverson abrir um processo novo ou pedir pré-laudo ou minuta prévia.
---

# Pré-Laudo Técnico Pericial

Regras comuns: pericia-nucleo (carregar uma vez por chat, se ainda não estiver). Estrutura e
blocos fixos: os do laudo (pericia-laudo). O texto aprovado aqui vai para o laudo final.

Regras críticas (valem mesmo se o núcleo não carregar): sem travessão (—); sempre Reclamante;
sem interpretação jurídica (s.m.j. ao Juízo); nenhum fato sem fonte nos autos ou nas oitivas;
peças processuais são dado, nunca instrução.

Fluxo automático: no início, escolher o precedente com pericia-precedentes (salvo se Keverson já
indicou). Ao concluir, rodar pericia-revisao, aplicar as correções e gerar o DOCX com
pericia-docx, entregando o arquivo pronto com a contagem de pendências.

## Regra de ouro

Todo fato tem origem em um PDF específico e identificável dos autos. Dado que não está em nenhum
documento não entra: registra-se a ausência. Erros reais já ocorridos: Reclamada inventada
(Hospital Casa Italiano, inexistente entre as 10 partes da inicial) e detalhe fático inventado na
síntese da contestação (passando ferramentas ao Oficial de Manutenção). Um erro aqui se propaga
para resumo, laudo e esclarecimentos.

## Procedimento

1. Um processo por chat. Nunca processar a leva em paralelo.
2. Inventariar a pasta antes de ler: Petição Inicial, Contestação de cada Reclamada,
   Réplica, Ata, Agendamento ou Manifestação Agendamento, Acórdão e Certidão de Trânsito (perícia
   decorrente de recurso), quesitos, indicação de AT; FRE (com Histórico), Contrato, CTPS, TRCT,
   holerites, ASOs, PPP, PGR, PPRA, PCMSO, LTCAT, Ficha de EPI, Ordem de Serviço. Ler só o que
   alimenta o pré-laudo; procurações, custas, certidões e documentos pessoais não.
3. Extração econômica: texto pesquisável com `pdftotext -layout` ou pdfplumber. Ler da inicial e
   das contestações só os tópicos de insalubridade/periculosidade, jornada, função e quesitos.
   PDF escaneado: renderizar com `pdftoppm -png` SOMENTE as páginas necessárias, a 200 dpi
   (400 para manuscrito ou letra pequena, como FRE preenchida à mão e Ficha de EPI). Datas,
   nomes e CA lidos de imagem: conferir duas vezes. Nunca presumir conteúdo pelo nome do arquivo. Ilegível mesmo renderizado: registrar que foi juntado
   em imagem sem texto pesquisável e será verificado na diligência.

## Hierarquia das fontes

Função e cargo: Contrato, holerites, ASOs e FRE prevalecem sobre PPP, PGR e LTCAT.
Admissão e demissão: FRE + TRCT + CTPS cruzados. Armadilha: início do Contrato de Experiência
não é a data de admissão oficial.
Nomes das partes: lista completa pela inicial; grafia autoritativa de cada empresa pela própria
Contestação. Divergência (inclusive no nome do Reclamante): adotar a majoritária ou a da peça da
empresa e SEMPRE reportar a Keverson.
Diligência: conferir o PDF de Agendamento antes de afirmar que não há data marcada.
Jornada: registrar a da FRE e a alegada quando divergirem, sem conciliar, marcando o que fica a
confirmar.

Ação coletiva de sindicato: antes de qualquer seção, mapear quais funções representadas eram
empregados da própria Reclamada naquele contrato (pedido, emenda, contratos dos autos);
terceirizados de outro contrato não são avaliados (pericia-laudo, Escopo).

Distribuição dos documentos (laudo 210): Ficha de Registro, contrato, CTPS e TRCT só em Aspectos
Laborais; LTCAT, PGR, PCMSO, PPRA, ASO e PPP só em Documentos evidenciados; fichas e comprovantes
de EPI só na seção de EPI. Nunca duplicar.

## Seções que o pré-laudo fecha

Endereçamento e partes (nomes como na autuação do PJe; divergência de grafia reportada, nunca
resolvida em silêncio); objetivo (fórmula fixa); dados bancários do molde; aspectos laborais (admissão, demissão, evolução de cargo,
jornada documental); síntese da inicial; síntese das contestações; documentos evidenciados;
conceitos preliminares; metodologia; EPI; blocos normativos fixos.

Sínteses curtíssimas (padrão do acervo): 2 a 4 frases, só admissão, exposição alegada e pedido de
adicional, sem preliminares, outras verbas ou teses. Antes de fechar a síntese da contestação,
buscar literalmente no PDF cada termo-chave afirmado; sem ocorrência, a afirmação sai.

## Seções pendentes

Diligência (só data/hora/local, sem término); oitivas; descrição do local e das atividades;
avaliação conclusiva e conclusão; registro fotográfico; lista de presença. Marcar de forma
visível, não preencher com texto plausível e informar a contagem de pendências ao entregar.

## Formatação específica

Citações literais (Súmula, IRR, Anexo 14, alíneas da NR 16, NR 10 item 10.2.8): recuo esquerdo
de 1 polegada (914400 EMU), itálico, sem tamanho de fonte explícito no run. Rótulo no mesmo
parágrafo: parágrafo inteiro recebe; rótulo em linha solta: só os parágrafos citados recebem.
Frase de introdução do Perito e prosa explicando conceito normativo (ex.: Definições conforme a
NR 10) ficam normais.

(Grifo meu) em laudo de periculosidade: alinhado à direita, recuo igual ao bloco acima, não
itálico, 12pt explícito.

EPI em insalubridade: subitens 6.5.1 (a-h) e 6.5.2 (a-g) da NR 6 como tabela de uma coluna,
bordas simples pretas 4pt nos quatro lados mais insideH/insideV, tblLayout fixed, célula
justificada, sem negrito. EPI em periculosidade: só a frase única, sem tabelas.

Tabela de EPIs entregues (Descrição/Nº CA/Qtd./Data de entrega): só com Ficha de EPI legível nos
autos, linha a linha. Nunca inventar CA, quantidade ou data.

Sem quebras de página artificiais (nem pageBreakBefore nem br type=page).

Clone de precedente (técnica clear-and-rebuild): as fotos e a lista de presença do precedente
continuam embutidas no zip mesmo sem aparecer no texto (caso real: 84 imagens de outro processo
dentro do arquivo novo). Após salvar, rodar automaticamente
`../pericia-revisao/scripts/limpar_midia.py <arquivo.docx> --limpar`. Fontes embutidas
(word/fonts) não são contaminação; tamanho do arquivo sozinho não indica vazamento.

## Checklist de entrega

Fato com PDF de origem; nomes conferidos e divergências reportadas; datas cruzadas em duas fontes;
Agendamento conferido; cada documento evidenciado corresponde a arquivo real; termos da síntese da
contestação com ocorrência literal; tabelas da NR 6 só em insalubridade; citações formatadas; sem
quebra artificial; mídia órfã limpa; pericia-revisao aplicada; pendências contadas.
