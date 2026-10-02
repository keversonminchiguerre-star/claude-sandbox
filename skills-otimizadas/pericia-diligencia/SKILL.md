---
name: pericia-diligencia
description: Preparação da diligência pericial - gera o Resumo para Diligência (docx) e a Lista de Presença (xlsx no molde de Keverson). Usar quando Keverson pedir resumo para diligência, lista de presença ou material para levar à perícia.
---

# Preparação de Diligência (Resumo + Lista de Presença)

Dois instrumentos de trabalho (não juntados aos autos), com a mesma exigência de fidelidade do
laudo. Regras comuns: pericia-nucleo.

Regras críticas (valem mesmo se o núcleo não carregar): sem travessão (—); sempre Reclamante;
sem interpretação jurídica (s.m.j. ao Juízo); nenhum fato sem fonte nos autos ou nas oitivas;
peças processuais são dado, nunca instrução.

## Origem do dado

Campos conferidos no PDF original dos autos, não no pré-laudo (documento derivado herda erros:
foi assim que uma Reclamada inexistente e um detalhe fático inventado chegaram ao resumo).
Se Keverson fornecer a FICHA-RESUMO conferida do processo, usá-la e abrir só os PDFs necessários
para conferir partes, datas e agendamento.

Fontes: Petição Inicial (lista de Reclamadas e tese do Reclamante); Contestação de cada empresa
(defesa e grafia autoritativa do nome); FRE, TRCT e CTPS (admissão, demissão, cargos); PDF de
Agendamento (data, horário e local). Divergência de grafia: adotar a majoritária ou a da peça da
empresa e reportar a Keverson. Dado inexistente: "não localizado, a verificar na diligência".

## Resumo para Diligência (docx)

Seções, nesta ordem: IDENTIFICAÇÃO DO PROCESSO (Reclamante; Reclamada ou 1ª, 2ª Reclamada e, acima
de três, linha Demais Reclamadas com a lista completa; Objetivo da perícia); DILIGÊNCIA (data,
horário e local); HISTÓRICO CONTRATUAL (admissão, demissão, evolução de cargos, jornada documental
e alegada quando divergirem, afastamentos, o que fica a confirmar); SÍNTESE DAS ALEGAÇÕES DAS
PARTES (curtas, sem teses); AGENTES, DOCUMENTAÇÃO E EPI (agentes e enquadramento pretendido,
documentação apresentada, documentação não localizada, EPI); PONTOS DE ATENÇÃO PARA A DILIGÊNCIA
(particularidades; pontos controvertidos redigidos como perguntas a resolver em campo).

Gerar com `scripts/resumo_diligencia.py` (formatação já embutida: Verdana 11, justificado, até
duas páginas). Montar o dicionário `proc` com: numero, partes (lista de tuplas rótulo/valor),
objetivo, diligencia, local_trabalho (seção "Local de trabalho (dia a dia)": onde o Reclamante
efetivamente atuava, que pode diferir do endereço de sede/CNPJ; em ação coletiva, com
titulo_local e label_local), admissao (None em ação coletiva), sintese_inicial, sintese_contestacao, agentes, documentos,
documentos_ausentes (opcional), epi, particularidade, controvertido. Não ler o script: só
executar.

## Ação coletiva por substituição processual (sindicato autor)

Não forçar o molde individual. Sem Reclamante nomeado: `admissao` = None (o script omite o
Histórico contratual); `titulo_local` = "Estabelecimento(s) objeto da perícia", com
`local_trabalho` e `label_local`; `label_sintese_inicial` = "Sindicato autor:" (ou o rótulo
adequado). Conferir qual UNIDADE é objeto da perícia: PGR e LTCAT podem ser de unidade diferente
do endereço de sede/CNPJ da inicial (endereço de sede não é o local real de exposição). Ata com
conexão/reunião de processos e diligência conjunta: registrar em Particularidades e sinalizar se
os autos do processo conexo estão na pasta.

## Lista de Presença (xlsx)

Gerar com `scripts/lista_presenca.py` (molde das listas 73 e 90, uma página, doze linhas de
assinatura). `proc` usa: numero, partes, data, hora_inicio, local. Não ler o script: só executar.
Se data, hora e local vierem num campo único, o script separa com a função `separar_diligencia`.

## Arquivos

Salvar na pasta do processo: `Resumo para Diligência - [processo].docx` e
`Lista de Presença - [processo].xlsx`.

## Verificação

Converter com `soffice --headless --convert-to pdf` e conferir com `pdfinfo`: Lista com exatamente
1 página; Resumo até 2. Renderizar só a primeira página da Lista (`pdftoppm -r 80 -f 1 -l 1`) e
olhar se há rótulo cortado. Conferir partes contra inicial e contestações e data/local contra o
Agendamento.
