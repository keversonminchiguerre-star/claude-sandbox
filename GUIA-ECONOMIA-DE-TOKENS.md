# Guia de economia de tokens: perícias trabalhistas

Guia prático para fazer o limite do Claude render mais no fluxo de perícia
(pré-laudo, diligência, laudo, esclarecimentos, manifestações, cálculo).

---

## 1. Por que o limite acaba rápido

O Claude não "lembra" da conversa: **a cada nova mensagem, todo o histórico do
chat é reenviado e contado de novo**. Isso inclui os PDFs anexados, as skills
carregadas e todas as respostas anteriores.

Exemplo: um chat com os autos em PDF (~80 mil tokens) e 15 mensagens de ida e
volta consome perto de **1,2 milhão de tokens**, e não 80 mil.

As cinco maiores causas de consumo, em ordem:

1. **Chats longos** (um processo inteiro, ou vários processos, no mesmo chat).
2. **PDFs dos autos inteiros**, principalmente escaneados (cada página vira imagem).
3. **Pedir o laudo inteiro de novo** a cada pequeno ajuste.
4. **Modelo mais caro** (Opus) e raciocínio estendido em tarefas simples.
5. **Conectores ligados sem necessidade** (Gmail, Agenda, Drive, Zoom): as
   definições das ferramentas entram em toda mensagem.

---

## 2. As 10 regras (resumo para colar na parede)

| # | Regra | Economia típica |
|---|-------|-----------------|
| 1 | **Um chat por etapa de um processo** (pré-laudo, oitivas, conclusão, quesitos...). Nunca dois processos no mesmo chat. | Muito alta |
| 2 | **Envie só as peças necessárias** dos autos, não o PDF completo. | Muito alta |
| 3 | **Prefira texto a PDF escaneado.** Copie e cole o trecho ou use PDF pesquisável. | Alta |
| 4 | **Peça só o trecho alterado**, nunca "me manda o laudo todo de novo". | Alta |
| 5 | **Edite a mensagem** (ícone de lápis) em vez de mandar "não, não era isso". | Média |
| 6 | **Junte pedidos** numa mensagem só, em lista numerada. | Média |
| 7 | **Feche o chat com um resumo** e abra um novo colando o resumo. | Alta |
| 8 | **Escolha o modelo pela tarefa** (ver seção 5). | Alta |
| 9 | **Desligue conectores e raciocínio estendido** quando não usar. | Média |
| 10 | **Gere o DOCX uma vez só**, no fim, com o texto já revisado. | Média |

---

## 3. Fluxo recomendado por processo

Cada caixa é um chat novo. O que passa de um chat para o outro é um
**resumo curto**, não o histórico.

```
[Chat 1] Pré-laudo
   Entrada: Petição Inicial (só fatos e pedidos), Contestação (só a parte
            técnica), PPP/FRE/ficha de EPI.
   Saída:   pré-laudo + FICHA-RESUMO do processo (ver modelo abaixo)

[Chat 2] Diligência
   Entrada: FICHA-RESUMO
   Saída:   resumo para diligência + lista de presença

[Chat 3] Laudo (oitivas + avaliação + conclusão)
   Entrada: FICHA-RESUMO + anotações da diligência
   Saída:   texto das seções

[Chat 4] Quesitos
   Entrada: FICHA-RESUMO + conclusão do laudo + enunciados dos quesitos

[Chat 5] Revisão final + DOCX
   Entrada: texto final consolidado

[Chat 6+] Esclarecimentos / Manifestação (quando houver)
   Entrada: FICHA-RESUMO + conclusão do laudo + só a impugnação/parecer do AT
```

### Modelo de FICHA-RESUMO (peça ao fim do Chat 1)

> Faça uma FICHA-RESUMO deste processo em no máximo 300 palavras, para eu
> colar em chats futuros: nº do processo, partes, função e período,
> local de trabalho, agentes alegados, tese da Reclamada, documentos
> relevantes (PPP, LTCAT, fichas de EPI com CA e datas), pontos
> controvertidos e pendências para a diligência.

Essa ficha substitui os autos nos chats seguintes. É aqui que está a maior
economia.

---

## 4. Como mandar os autos sem desperdício

- **Não anexe o processo completo do PJe.** Separe só as peças úteis:
  Petição Inicial, Contestação, PPP/LTCAT, fichas de EPI, despacho de
  nomeação, quesitos. Procurações, custas, atas, certidões e documentos
  pessoais não ajudam e custam caro.
- **Corte as páginas** no próprio leitor de PDF (Imprimir → páginas X a Y →
  Salvar como PDF) ou peça ao Claude, em um chat curto e separado, para
  extrair só o texto das peças e devolver em texto puro.
- **PDF escaneado custa várias vezes mais** que PDF com texto. Se a peça for
  curta, copiar e colar o texto é o mais barato.
- **Na Petição Inicial e na Contestação**, normalmente só interessam os
  tópicos de insalubridade/periculosidade e os quesitos. Envie só esses
  trechos.
- **Laudo precedente**: não anexe o laudo-base inteiro. Mande só a seção que
  vai servir de modelo (ex.: só a avaliação do Anexo 14).

---

## 5. Qual modelo usar em cada tarefa

| Tarefa | Modelo sugerido |
|--------|-----------------|
| Extrair texto, organizar peças, lista de presença, resumo para diligência | **Haiku** |
| Oitivas, quesitos simples, revisão anti-IA, manifestação curta, formatação | **Sonnet** |
| Avaliação técnica complexa (NR 15/16), esclarecimentos contra parecer de AT, liquidação de cálculo | **Opus** |

Deixe o **raciocínio estendido** desligado por padrão e ligue só para
avaliação técnica ou resposta a AT.

---

## 6. Frases prontas que economizam

Cole no fim dos pedidos conforme o caso:

- **"Responda só com o texto do trecho, sem introdução nem comentários."**
- **"Mostre apenas os parágrafos que mudaram."**
- **"Não repita o laudo; devolva só a seção [X]."**
- **"Se faltar alguma informação, pergunte antes de redigir."** (evita
  gerar um texto inteiro errado e ter de refazer)
- **"Faça os itens 1 a 4 abaixo de uma vez:"** (pedidos em lote)
- **"Resuma este chat em até 300 palavras para eu continuar em um chat novo."**

---

## 7. Skills e conectores

- As skills só são carregadas quando o assunto aciona cada uma, mas
  **pedidos vagos acionam várias ao mesmo tempo** (ex.: "faça o laudo e
  revise" pode acionar laudo, revisão, docx, precedentes e quesitos de uma
  vez). Seja específico: **"Use a skill pericia-oitivas para..."**.
- A skill **pericia-docx** lê o laudo mais recente do acervo para copiar a
  formatação. Use-a **uma vez**, no fim, com o texto já aprovado. Ajustes
  de texto devem ser feitos antes, em texto, e não regerando o DOCX.
- A **pericia-revisao** deve rodar sobre o texto final, uma vez, e não a cada
  seção redigida.
- **Desligue Gmail, Agenda, Drive e Zoom** nos chats de redação (menu de
  ferramentas/conectores). Ligue só no chat em que for usar.

---

## 8. Projetos (claude.ai)

- Se usar um Projeto para as perícias, coloque nos "conhecimentos do projeto"
  **só material fixo e enxuto**: modelo de estrutura, lista de frases
  proibidas, padrões de redação. **Não coloque autos de processos** nem
  dezenas de laudos antigos.
- Instruções do projeto curtas (até ~1 página). Tudo que estiver ali é
  reenviado em todas as mensagens de todos os chats do projeto.

---

## 9. Checklist rápido antes de enviar

- [ ] Este chat é só deste processo e desta etapa?
- [ ] Mandei só as peças/páginas necessárias?
- [ ] Usei a FICHA-RESUMO em vez dos autos?
- [ ] Pedi só o trecho, sem reescrever tudo?
- [ ] O modelo está adequado à tarefa?
- [ ] Os conectores que não vou usar estão desligados?
- [ ] O chat passou de ~15 mensagens? Então resumir e abrir outro.
