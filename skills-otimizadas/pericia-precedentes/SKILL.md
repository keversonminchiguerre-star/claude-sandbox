---
name: pericia-precedentes
description: Escolhe no acervo de Keverson o laudo precedente mais próximo de um caso novo (base de redação e molde). Usar uma vez por processo, quando Keverson pedir precedente, caso parecido ou laudo-base, ou no início do pré-laudo se ele não tiver indicado o precedente.
---

# Busca de Precedentes no Acervo

Executar uma vez por processo. Depois de escolhido, o precedente fica registrado no chat (e na
FICHA-RESUMO) e não se repete a busca.

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
4. Definir o PRECEDENTE DE REDAÇÃO (caso mais parecido) e o MOLDE FÍSICO (sempre o laudo mais
   recente, hoje o 169, usado pela pericia-docx). Podem ser diferentes.
5. Reportar em poucas linhas: precedente, motivo e fórmulas reaproveitadas.

## Casamentos conhecidos (dispensam a busca)

Lanchonete com banheiros, negativa: redação 140/118/119, molde 169. Hotel, camareira: 119.
Clube ou igreja com possível grande circulação: 169 e 91 (Súmula 448 ao Juízo). Cozinha com
calor: 172 e 149 (negativos com IBUTG) ou 113 e 114. Câmara fria em mercado: 151, 150, 163.
Hospital, enfermagem: 152, 158, 166; Covid no período: 103, 111, 117, 131, 132, 144, 152, 158,
165. Gerador ou inflamáveis: 143 e 146 (negativos), 127 e 107 (devidos). Eletricidade: 167 e 168
(devidos), 138 (negativo, extra-baixa tensão).

## Honestidade

Nenhum precedente casa bem: dizer isso a Keverson e aplicar a lógica geral (pericia-laudo ou
avaliacao-nr16), com uma busca nos arquivos do projeto pelos critérios do agente. Não forçar
precedente errado.
