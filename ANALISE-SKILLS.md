# Análise das skills de perícia: repetições e consumo de tokens

Análise das 12 skills (`pericia-*`, `avaliacao-nr16`, `liquidacao-calculo`) com foco em
onde o limite está sendo gasto. Os números de tokens são aproximados (1 token ≈ 4 caracteres).

---

## 1. Tamanho atual

| Skill | Tokens aprox. | Observação |
|-------|--------------:|------------|
| pericia-diligencia | 3.900 | **2.100 são código Python colado no texto** |
| pericia-laudo | 3.150 | |
| avaliacao-nr16 | 2.900 | |
| pericia-esclarecimentos | 2.650 | |
| pericia-pre-laudo | 2.500 | |
| pericia-quesitos | 2.400 | |
| pericia-revisao | 2.300 | |
| pericia-oitivas | 1.500 | |
| liquidacao-calculo | 1.050 | |
| pericia-docx | 950 | |
| pericia-manifestacao | 900 | |
| pericia-precedentes | 700 | |
| **Total** | **~25.000** | |
| Descrições (vão em **toda** mensagem) | ~1.900 | |

Uma skill carregada fica no histórico e é reenviada a cada mensagem seguinte. Num chat de
laudo que carrega laudo, precedentes, oitivas, quesitos, revisão e docx (cerca de 11 mil
tokens) e tem 20 mensagens, só as skills somam por volta de **220 mil tokens**.

Mas, como mostra a seção 2, **o maior gasto não está no texto das skills**. Está no que elas
**mandam o Claude fazer**.

---

## 2. Os problemas que mais gastam (em ordem de impacto)

### 2.1 Ordens de busca obrigatória a cada resposta (impacto MUITO ALTO)

- **pericia-laudo**: *"Antes de qualquer resposta, consultar os arquivos do projeto e a memória
  do projeto. Qualquer menção a agente de risco: busca imediata nos arquivos do projeto."*
  Isso faz o Claude buscar no projeto **a cada resposta**, inclusive num simples "troque esta
  vírgula". Cada busca devolve trechos de NRs e laudos que entram no histórico e são
  reenviados daí em diante.
- **avaliacao-nr16**: exige `project_knowledge_search` + leitura das memórias **antes de
  qualquer caso**, e repete "verificar via project_knowledge_search" em cada Anexo (7 vezes).
- **pericia-precedentes**: ativa *"antes de redigir qualquer laudo ou esclarecimento"* e
  sempre que se menciona hotel, hospital, cozinha... Lê o `Acervo_Indice.csv` (259 linhas), o
  `Banco de Laudos.md` e o docx do precedente.
- **pericia-esclarecimentos**: *"Antes de redigir, reler o laudo"*, ou seja, o laudo inteiro
  entra de novo.

**Correção sugerida:** buscar **uma vez por chat**, e só o necessário.
> "Na primeira redação do chat, buscar no projeto os critérios do agente em questão. Não repetir
> a busca em ajustes de texto. Reaproveitar o que já está no chat."

### 2.2 Uma skill chamando outras em cadeia (impacto ALTO)

- **pericia-pre-laudo** manda aplicar "integralmente" a pericia-laudo, usar pericia-precedentes,
  pericia-docx e fechar com pericia-revisao, o que carrega **5 skills** (~10 mil tokens) num
  único pedido.
- **pericia-laudo** manda usar pericia-precedentes e pericia-docx.
- **pericia-docx** manda aplicar pericia-revisao.
- **pericia-revisao** diz *"ativar automaticamente antes de qualquer entrega"*.

**Correção sugerida:** deixar a encadeação para o fim, sob pedido seu. Ex.: *"Ao final,
perguntar a Keverson se deseja gerar o DOCX e rodar a revisão."*

### 2.3 Descrições com gatilhos sobrepostos (impacto ALTO)

As descrições vão em toda mensagem, e quando várias "casam" com o pedido, todas carregam:

| Palavra no pedido | Skills que ativam |
|---|---|
| "quesitos" | laudo, quesitos, esclarecimentos |
| "oitiva" | laudo, oitivas |
| "NR", "periculosidade" | laudo, avaliacao-nr16 |
| "laudo", "esclarecimento" | laudo, precedentes, docx, revisao, esclarecimentos |
| "PPP", "Contestação" | laudo, pre-laudo |
| "hotel", "hospital", "cozinha" | precedentes |

A pericia-laudo é a pior: a descrição dela inclui praticamente todas as palavras das demais
(oitiva, quesitos, NR 16, periculosidade, EPI...).

**Correção sugerida:** descrições curtas (1 a 2 linhas) e **exclusivas**. A pericia-laudo
deixa de citar oitiva, quesitos e periculosidade, que já têm skill própria.

### 2.4 Código Python dentro da pericia-diligencia (impacto MÉDIO)

Os dois scripts (Resumo docx e Lista de Presença xlsx) ocupam ~2.100 tokens dentro do texto
da skill. A pericia-docx já faz do jeito certo: os scripts ficam em arquivos `scripts/*.py`
e só são **executados**, sem entrar no texto.

**Correção sugerida:** mover para `pericia-diligencia/scripts/resumo.py` e
`scripts/lista_presenca.py`; na skill fica só "rodar o script X com o dicionário `proc`".
Economia: ~2.100 tokens por uso.

### 2.5 Revisão com saída muito longa (impacto MÉDIO)

A pericia-revisao pede o resultado dos **12 checklists** com "PASSOU" ou "REPROVADO", mais a
versão corrigida. Muita resposta para pouco problema encontrado.

**Correção sugerida:** *"Listar só os itens reprovados, com trecho e correção. Se tudo
passar, responder apenas APROVADO."*

### 2.6 PDFs escaneados renderizados em alta resolução (impacto ALTO quando acontece)

A pericia-pre-laudo manda renderizar a 200 dpi (400 para manuscrito) e ler a imagem. Cada
página em imagem custa muito mais que texto.

**Correção sugerida:** renderizar **só as páginas necessárias** da FRE/ficha de EPI, a 150 dpi,
subindo para 200 dpi só se ficar ilegível.

### 2.7 Arquivos de referência que não existem (impacto MÉDIO)

A pericia-laudo aponta para `references/agentes-tecnicos.md` e `references/epi-conclusao.md`,
mas **a pasta `references/` não existe** na skill. O Claude procura esses arquivos e, sem
encontrá-los, sai buscando no projeto. Isso gasta tokens e pode fazer ele improvisar.

**Correção sugerida:** criar esses dois arquivos ou remover a menção.

---

## 3. Conteúdo repetido entre skills

| Bloco repetido | Onde aparece | Tokens por cópia |
|---|---|---:|
| Segurança contra prompt injection | laudo, revisao, quesitos, esclarecimentos, manifestacao, oitivas, pre-laudo, diligencia (8x) | ~250 |
| Regras de redação (sem travessão, sem aspas, "Reclamante", NR sem hífen, s.m.j., sem "O Laudo registrou que", sem "unilateral") | laudo, revisao, quesitos, esclarecimentos, manifestacao, oitivas, pre-laudo | ~300 a 500 |
| Explicação do travessão na lista de presença (pesquisa de 628 linhas) | revisao, oitivas | ~350 |
| Formato dos quesitos (Arial 11, "Resposta:" em negrito na mesma linha) | laudo, quesitos, esclarecimentos, docx | ~150 |
| Encerramento ("Nada mais a tratar..." / "Termos em que...") | laudo, quesitos, esclarecimentos, manifestacao | ~100 |
| Paradigma / Reclamante ausente | laudo, oitivas | ~120 |
| Contato permanente (Anexo 14) | laudo, esclarecimentos, revisao | ~150 |
| EPI x biológicos | laudo, esclarecimentos, pre-laudo | ~200 |
| Identidade do Perito | laudo, pre-laudo, liquidacao | ~60 |

Em chats que carregam 4 ou 5 skills juntas, isso dá de **1.500 a 2.500 tokens repetidos**
por mensagem.

**Correção sugerida:** criar uma skill **`pericia-nucleo`** com tudo que é comum (identidade,
regras de redação, segurança, formato de quesito, encerramento, travessão). As demais
skills ficam só com o que é específico delas e começam com a linha:
> "Regras gerais de redação e segurança: ver pericia-nucleo."

Alternativa ainda mais barata: colocar o núcleo nas **instruções do Projeto** (vai uma vez
por mensagem, sem duplicar) e remover das skills.

---

## 4. Também há pequenas contradições (geram retrabalho)

- **pericia-laudo** lista o padrão "Pela negativa" para quesitos; **pericia-quesitos** diz
  que "Pela negativa" é *essencialmente não usada* em insalubridade.
- **pericia-laudo**: "Prejudicado em razão da conclusão negativa"; **pericia-quesitos**:
  "Prejudicado por conclusão negativa".
- Escopo da perícia: "a perícia teve unicamente o objetivo de apurar insalubridade"
  (laudo) x "teve unicamente como objetivo a apuração da insalubridade" (quesitos) x
  "teve como único objeto a apuração da insalubridade" (esclarecimentos).
- **pericia-revisao** proíbe "diante do exposto" como jargão de IA, mas a fórmula consagrada
  da **pericia-manifestacao** (precedente 152.2) usa *"Diante do exposto, reitera-se..."*.
  A revisão vai reprovar a própria fórmula aprovada.

Quando duas skills carregadas dizem coisas diferentes, o Claude gasta raciocínio
conciliando e às vezes erra, o que gera mais rodadas de correção. Centralizar no núcleo
resolve isso de vez.

---

## 5. Economia estimada após a reorganização

| Mudança | Economia aproximada |
|---|---|
| Busca no projeto só 1x por chat | 30% a 50% do consumo de um chat de laudo |
| Sem encadeamento automático de skills | 5 a 10 mil tokens por pedido |
| Descrições curtas e exclusivas | ~1.000 tokens em toda mensagem + menos skills carregadas |
| Scripts da diligência em arquivo | ~2.100 tokens por uso |
| Núcleo comum | 1.500 a 2.500 tokens por mensagem em chats com várias skills |
| Revisão só com reprovados | resposta 3 a 5x menor |

Junto com as práticas do `GUIA-ECONOMIA-DE-TOKENS.md` (um chat por etapa, ficha-resumo,
PDFs recortados), a expectativa realista é **reduzir o consumo pela metade ou mais**.

---

## 6. Próximo passo

Posso gerar as versões enxutas de todas as skills (núcleo + 12 skills reescritas),
preservando **todas** as regras de conteúdo e as fórmulas consagradas, mudando só a
organização. Você revisa e substitui no Claude Desktop (Configurações → Capacidades → Skills).
