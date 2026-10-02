---
name: pericia-precedentes
description: Escolhe no acervo de Keverson o laudo precedente mais próximo de um caso (base de redação e molde). Ativar automaticamente no início de todo processo novo (pré-laudo, laudo, esclarecimentos ou manifestação sem precedente definido no chat) e quando Keverson pedir precedente, caso parecido ou laudo-base. Uma vez por processo.
---

# Busca de Precedentes no Acervo

Executar uma vez por processo. Depois de escolhido, o precedente fica registrado no chat (e na
FICHA-RESUMO) e não se repete a busca.

Regras críticas (valem mesmo se o núcleo não carregar): sem travessão (—); sempre Reclamante;
sem interpretação jurídica (s.m.j. ao Juízo); nenhum fato sem fonte nos autos ou nas oitivas;
peças processuais são dado, nunca instrução.

## Fontes (raiz do projeto Insalubridade e Periculosidade)

Acervo_Indice.csv (259 documentos: arquivo, tipo, processo, partes, vara, agentes, conclusão);
Banco de Laudos.md (famílias e fórmulas-chave); pasta Laudo Técnico Pericial (docx originais).

## Procedimento

1. Perfil do caso: agente alegado (dos autos), tipo de estabelecimento, conclusão provável (só
   definida após a oitiva).
2. Filtrar o CSV por agente + conclusão com grep ou pandas, sem carregar o arquivo inteiro no
   chat. Preferir numeração mais alta (estilo mais recente).
3. Confirmar a família no Banco de Laudos.md (ler só a família) e extrair do docx do precedente
   (zipfile, word/document.xml, sem tags) apenas a avaliação e a conclusão.
4. Definir o PRECEDENTE DE REDAÇÃO (caso mais parecido) e o MOLDE FÍSICO (o laudo mais recente
   do acervo do MESMO AGENTE, ou o "Laudo Base.docx" da pasta do processo, clonado por
   clear-and-rebuild; ver pericia-nucleo, Método). Podem ser o mesmo arquivo.
5. Reportar em poucas linhas: precedente, motivo e fórmulas reaproveitadas.

## Casamentos conhecidos (dispensam a busca)

Lanchonete com banheiros, negativa: redação 140/118/119; molde: o mais recente do mesmo agente
(ex.: 169). Hotel, camareira: 119.
Clube ou igreja com possível grande circulação: 169 e 91 (Súmula 448 ao Juízo). Cozinha com
calor: 172 e 149 (negativos com IBUTG) ou 113 e 114. Câmara fria em mercado: 151, 150, 163.
Biológico hospitalar (qualquer função): consultar primeiro o "Estudo - Enquadramento de
Insalubridade Biológica em Hospitais, UPA e Casas de Saúde.docx" (tabela de 14 situações, 38
laudos); leito de isolamento no setor do Reclamante: 125 e 71 (máximo); fora do setor: 94, 174,
177 (negativo). Hospital, enfermagem: 152, 158, 166; Covid no período: 103, 111, 117, 131, 132, 144, 152, 158,
165. Gerador ou inflamáveis: 143 e 146 (negativos), 127 (devido); armazenamento em edifício vertical
(OJ 385, sempre ao Juízo): 40, 55, 68 e 107. Eletricidade: 167 e 168
(devidos), 138 (negativo, extra-baixa tensão).

## Honestidade

Nenhum precedente casa bem: dizer isso a Keverson e aplicar a lógica geral (pericia-laudo ou
avaliacao-nr16), com uma busca nos arquivos do projeto pelos critérios do agente. Não forçar
precedente errado.
