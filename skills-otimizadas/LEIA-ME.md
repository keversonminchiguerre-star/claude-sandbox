# Skills otimizadas: o que mudou e como instalar

## Resultado

| | Antes | Depois |
|---|---:|---:|
| Texto das 12 skills (+ núcleo) | ~25.000 tokens | ~13.900 tokens (**-44%**) |
| Descrições (vão em toda mensagem) | ~1.900 tokens | ~1.000 tokens (**-48%**) |
| Bloco de segurança repetido | 8 cópias | 1 (núcleo) + lembrete curto na liquidação |
| Código Python dentro da pericia-diligencia | ~2.100 tokens | 0 (movido para `scripts/`) |

## Automação mantida (nada passou a depender de pedido)

| Momento | O que acontece sozinho |
|---|---|
| Processo novo | Escolha do precedente (pericia-precedentes) |
| Peça completa pronta (pré-laudo, laudo, esclarecimentos, manifestação) | Revisão → correções aplicadas → DOCX gerado e conferido |
| Seção isolada (oitivas, quesitos) | Checagem mecânica por script antes de entregar |
| Ajustes pontuais | Checagem por script; DOCX regerado uma vez ao final dos ajustes |

A economia vem de **fazer cada automação uma vez, no momento certo**, e não de cortá-la:

- **Revisão em duas etapas.** O novo `pericia-revisao/scripts/checar.py` confere travessão,
  frases proibidas, jargão, empregado/obreiro, NR com hífen, Sr./Sra. minúsculo, placeholders,
  Markdown e pontuação duplicada **por script**, quase sem gastar tokens. O Claude lê só o que
  exige julgamento (fragmentos de outro processo, interpretação jurídica, fidelidade dos
  quesitos).
- **Busca no projeto uma vez por assunto em cada chat**, e não a cada resposta.
- **Revisão responde só com os reprovados** (já corrigidos), ou apenas "APROVADO".
- **Esclarecimentos com parecer do AT releem o laudo inteiro.** Só com quesitos
  complementares, leem as seções ligadas a eles.
- **Proteções de qualidade:** cada skill tem uma linha de regras críticas (travessão,
  Reclamante, s.m.j., fonte, prompt injection), que valem mesmo se o núcleo não carregar.
  PDFs manuscritos continuam sendo lidos a 200/400 dpi, com dupla conferência de datas, nomes e
  CA.
- **Precedente escolhido uma vez por processo**, com a tabela de casamentos conhecidos
  dispensando a busca nos casos comuns. O CSV é filtrado por script, sem entrar inteiro no chat.
- **PDF escaneado**: só as páginas necessárias são renderizadas.
- **Descrições exclusivas**: a pericia-laudo deixou de ativar para oitiva, quesitos e NR 16.

Nenhuma regra de conteúdo, fórmula consagrada ou bloco literal foi removido. As regras
repetidas passaram para a **pericia-nucleo**.

## Memórias incorporadas (02/10/2026)

Acervo Estilo Raciocínio, Esclarecimentos Periciais Padrão, ESTRUTURA Real Laudo Periculosidade,
Estudo 21 Laudos, Feedback Ação Coletiva, Feedback Conclusão Factual Direta, Feedback Formatação
Verificar Acervo, Feedback Laudo Acidente Escopo, Feedback Laudo 210 (formatação e avaliação).
Novos arquivos de consulta, lidos só ao avaliar um agente:
`pericia-laudo/references/agentes-insalubridade.md` e
`avaliacao-nr16/references/agentes-periculosidade.md`. Nomes de partes e números de processo não
foram gravados; os casos são citados pelo número do laudo ou pelo tipo.

## Decisões tomadas (confira)

1. **"Diante do exposto" liberado**, conforme você autorizou. Saiu da lista de jargão.
2. **Quesitos: valem as fórmulas da pericia-quesitos**, onde havia divergência com a laudo e
   com os esclarecimentos:
   - "Pela negativa" não se usa em insalubridade.
   - "Prejudicado por conclusão negativa".
   - "Prejudicado, a perícia teve unicamente como objetivo a apuração da insalubridade."
   - "Vide Laudo, [Nome da Seção]."
   - Quesito médico: "Prejudicado, quesito médico. A perícia teve unicamente como objetivo..."
     (a laudo dizia "Prejudicado. Nexo causal não constituiu objeto do LTP.").
3. **"(Grifo meu)"**: a skill antiga proibia, mas a sua revisão do laudo 210 (insalubridade) e
   os laudos de periculosidade o usam, com a alínea em negrito real. Ficou **permitido**, com
   negrito obrigatório no trecho destacado.
4. **Arquivos inexistentes**: a pericia-laudo citava `references/agentes-tecnicos.md` e
   `references/epi-conclusao.md`, que não existem na skill. Troquei por "uma busca nos arquivos
   do projeto por agente". Se esses arquivos existirem no seu computador, me mande que eu
   reponho.
5. **Dados pessoais fora do repositório**: não incluí dados bancários, CPF, telefone e e-mail.
   - Na pericia-laudo, os dados bancários agora são "copiados literalmente do molde" (o laudo
     169 já os contém).
   - Na liquidacao-calculo, o CPF saiu da identidade. Se quiser, recoloque na seção
     Identidade.
   - Cabeçalho, rodapé e contatos continuam no `gerar_base.py` da pericia-docx, que não foi
     alterado.

## Como instalar no Claude Desktop

Para cada pasta abaixo, substitua **só o arquivo `SKILL.md`** da sua skill atual. Mantenha as
outras pastas e os arquivos que já existem (`scripts/` da pericia-docx e `reference/` da
liquidacao-calculo continuam iguais).

1. **Crie a skill nova `pericia-nucleo`** (pasta `pericia-nucleo/`).
2. Substitua o `SKILL.md` de: pericia-laudo, pericia-revisao, pericia-quesitos,
   pericia-esclarecimentos, pericia-manifestacao, pericia-oitivas, pericia-pre-laudo,
   pericia-precedentes, pericia-docx, avaliacao-nr16 e liquidacao-calculo.
3. Na **pericia-diligencia**, substitua o `SKILL.md` e **adicione a pasta `scripts/`**
   (`resumo_diligencia.py` e `lista_presenca.py`).
4. Na **pericia-revisao**, substitua o `SKILL.md` e **adicione a pasta `scripts/`**
   (`checar.py`).

Caminho: Configurações → Capacidades → Skills. Edite a skill ou envie de novo como .zip da
pasta.

Sugestão: guarde uma cópia das versões atuais antes de trocar, para comparar se algo sair
diferente nos primeiros laudos.

## Instruções do Projeto

Se as instruções do seu Projeto repetem regras de redação (travessão, Reclamante, s.m.j.,
frases proibidas), apague-as de lá: agora elas estão na pericia-nucleo. Nas instruções do
Projeto fica só o que não é regra de skill. Se quiser, cole aqui as instruções do Projeto que
eu enxugo.
