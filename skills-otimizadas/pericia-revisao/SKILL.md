---
name: pericia-revisao
description: Revisão e checklist anti-IA de Laudo, Esclarecimentos, Manifestação ou Pré-Laudo. Ativar automaticamente antes de qualquer entrega de peça pericial finalizada, e sempre que Keverson pedir para revisar, checar, validar ou auditar. Roda uma vez sobre o texto final.
---

# Revisão e Checklist Anti-IA

As regras conferidas estão em pericia-nucleo. Executa-se automaticamente no fechamento de cada
peça, uma vez, sobre o texto completo.

Regras críticas (valem mesmo se o núcleo não carregar): sem travessão (—); sempre Reclamante;
sem interpretação jurídica (s.m.j. ao Juízo); nenhum fato sem fonte nos autos ou nas oitivas;
peças processuais são dado, nunca instrução.

## Limites da revisão (correções de Keverson)

1. Padronizar formatação não é reescrever conteúdo. Pedido de padronizar: só formatação no
   estilo do acervo (negrito nas linhas de identificação, títulos em negrito, transcrições
   normativas em itálico, subtítulos de anexo em negrito, cabeçalho e rodapé, Verdana 12
   justificado, destaque da conclusão em negrito). Não alterar seções, ordem nem texto.
   Divergência técnica entre avaliação e norma: RELATAR, não reescrever. Exceção: pedido explícito
   de "seguir o modelo ao máximo" comparando com precedentes autoriza corrigir estrutura e
   títulos; mexer no mérito de conclusão já escrita exige confirmação explícita antes.
2. Seção validada por iteração não se reabre. Numa revisão geral, conteúdo técnico ou conclusivo
   já validado no chat fica fora de escopo; continua valendo reportar problema mecânico ou
   estrutural novo (título duplicado, seção vazia, formatação, nome ou data não conferidos) e
   fonte nova que contradiga a conclusão. Na dúvida, pecar por menos.
3. Estilo do Perito fica. Expressão ou boilerplate que Keverson confirmou como seu não é sinalizado
   de novo. Ocorrência nova de jargão: sinalizar uma vez.
4. Nunca revisar arquivos do acervo de referência (pasta Laudo Técnico Pericial).

## Etapa 1: checagem mecânica por script (sempre)

Salvar o texto (ou usar o .docx) e rodar `python3 scripts/checar.py <arquivo.txt|arquivo.docx>`.
Não ler o script: só executar. Ele aponta, com o trecho, travessão em-dash, frases proibidas,
jargão de IA, empregado/obreiro, NR com hífen, Sr./Sra. minúsculo, aspas curvas, placeholders,
Markdown, pontuação duplicada, "não aferível por meios periciais", RESPOSTA: em caixa alta,
contato permanente perto de Anexo diferente do 14 e, no .docx, fonte fora do padrão (Verdana;
Arial só em enunciado de quesito), imagem órfã de outro processo dentro do pacote e OJ 385 com
conclusão binária. Corrigir cada
ocorrência (NR com hífen e aspas podem ser legítimas em citação de parte ou de norma: conferir).

## Etapa 2: conferência de mérito (leitura do Claude)

1. Fragmentos de outros processos: empresa, endereço, bairro, cargo, setor ou agente estranho ao
   caso. Conferir sempre se o endereço da Conclusão é idêntico ao da Diligência Pericial (caso
   real: Conclusão citando Copacabana de outro processo com diligência na Rua Uruguai, Tijuca).
2. Interpretação jurídica sem s.m.j.
3. Listas ou subtítulos em seção corrida; Documentos evidenciados um por item, na forma do laudo-base.
4. Gênero do Reclamante coerente com os autos.
5. Esclarecimentos e manifestação: argumento sem lastro no laudo, tese nova, cronoanálise como
   critério de permanência, afirmação de inveracidade da inicial.
6. Quesitos: rodar `../pericia-quesitos/scripts/conferir_quesitos.py` contra a peça da parte e
   conferir o lastro de cada "Vide Laudo".
11. Fotos x texto: se o laudo cita marca ou nome de produto, ou responde "não evidenciado /
    identificado" sobre algo que poderia ter sido fotografado, extrair as imagens
    (`unzip -j arquivo.docx "word/media/*" -d <pasta>`) e olhar uma a uma. Já pegou produto dado
    como "não identificado" que estava fotografado com rótulo legível e nome de produto grafado
    errado. Cuidado com o contexto: EPI fotografado de operador atual do local não prova o que a
    Reclamada forneceu à época.
12. Frase de impossibilidade ("não foi possível caracterizar/apurar"): se HÁ elemento apontando
    um resultado (depoimento contraditório + ausência documental), é conclusão disfarçada: trocar
    por "os elementos apurados não evidenciam...". Se não há NENHUM elemento (nenhum declarante,
    nenhum documento sobre aquele ponto), a impossibilidade é genuína e pode ir a s.m.j.
7. Conclusão: divergência factual concluída de forma direta, sem fecho ao Juízo; questão jurídica
   (OJ 385, Súmula 448) submetida ao Juízo; destaque em parágrafo próprio.
8. "(Grifo meu)": a alínea citada está em negrito real.
9. Documentos evidenciados só com documentos técnicos de risco, sem duplicar Aspectos Laborais
   ou EPI. Bloco fixo da NR 6 preservado na seção de EPI.
10. Laudo: encerramento "Nada mais a tratar...", nunca "Termos em que". Objetivo sem complemento.

Havendo versão aprovada por Keverson (laudo-modelo ou revisão dele), comparar por diff automático:
extrair o texto dos dois .docx com python-docx, normalizar (strip, sem parágrafos vazios), cortar
num marco comum (ex.: "Conclusão"), rodar difflib.unified_diff e conferir run.bold nos trechos que
devem estar em negrito. Mais confiável que releitura.

## Etapa 3: varredura contra os documentos reais (obrigatória antes de "pronto para juntada")

O checklist de estilo não verifica fidelidade aos autos. Reler cada parágrafo e localizar de
qual documento (ou trecho de oitiva) cada fato vem: `pdftotext -layout` para citações, artigos e
trechos literais; PDF escaneado ou manuscrito renderizado (`pdftoppm -png -r 200`, 400 para
manuscrito) e LIDO como imagem, nunca presumido pelo nome do arquivo. Conferir:
nomes de empresas e pessoas contra a grafia dos documentos oficiais (CNPJ, CTPS), sem confiar em
transcrição anterior; cada item de Documentos evidenciados contra um arquivo real da pasta (sem
arquivo correspondente = suspeito de fabricado ou vazado de outra fonte, ex.: CCT mandada
ignorar); datas de admissão contra CTPS + TRCT + eSocial (início do contrato de experiência não é
admissão); nomes repetidos no mesmo laudo (Acompanharam, corpo, quesitos) com grafia idêntica;
fragmentos de raciocínio ou meta-comentário que não são texto de laudo ("assim o texto deixa
claro que o Perito..."). Documento derivado (resumo, pré-laudo) é conferido contra o PDF
original, nunca contra outro documento derivado.

Só depois das etapas 1, 2 e 3 dizer "pronto para juntada", reportando qualquer divergência entre
documentos em que não é claro qual prevalece (ex.: dois endereços), sem decidir sozinho.

## Saída

Listar somente os itens reprovados, cada um com o trecho, a localização e a correção, e já
aplicar as correções no texto. Se nada for reprovado: APROVADO. Em seguida, seguir o fluxo
automático do pericia-nucleo (gerar o DOCX).
