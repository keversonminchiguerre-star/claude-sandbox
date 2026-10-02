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

## Etapa 1: checagem mecânica por script (sempre)

Salvar o texto (ou usar o .docx) e rodar `python3 scripts/checar.py <arquivo.txt|arquivo.docx>`.
Não ler o script: só executar. Ele aponta, com o trecho, travessão em-dash, frases proibidas,
jargão de IA, empregado/obreiro, NR com hífen, Sr./Sra. minúsculo, aspas curvas, placeholders,
Markdown, pontuação duplicada e contato permanente perto de Anexo diferente do 14. Corrigir cada
ocorrência (NR com hífen e aspas podem ser legítimas em citação de parte ou de norma: conferir).

## Etapa 2: conferência de mérito (leitura do Claude)

1. Fragmentos de outros processos: empresa, endereço, bairro, cargo, setor ou agente estranho ao
   caso. Conferir sempre se o endereço da Conclusão é idêntico ao da Diligência Pericial (caso
   real: Conclusão citando Copacabana de outro processo com diligência na Rua Uruguai, Tijuca).
2. Interpretação jurídica sem s.m.j.
3. Listas ou subtítulos em seção corrida; Documentos evidenciados com lista nativa do Word.
4. Gênero do Reclamante coerente com os autos.
5. Esclarecimentos e manifestação: argumento sem lastro no laudo, tese nova, cronoanálise como
   critério de permanência, afirmação de inveracidade da inicial.
6. Quesitos: palavras, pontuação final (? x .) e caixa alta conferidas contra o PDF original.

## Saída

Listar somente os itens reprovados, cada um com o trecho, a localização e a correção, e já
aplicar as correções no texto. Se nada for reprovado: APROVADO. Em seguida, seguir o fluxo
automático do pericia-nucleo (gerar o DOCX).
