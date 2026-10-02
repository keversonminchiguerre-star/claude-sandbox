# Skills otimizadas: o que mudou e como instalar

## Resultado

| | Antes | Depois |
|---|---:|---:|
| Texto das 12 skills (+ núcleo) | ~25.000 tokens | ~12.900 tokens (**-48%**) |
| Descrições (vão em toda mensagem) | ~1.900 tokens | ~1.000 tokens (**-48%**) |
| Bloco de segurança repetido | 8 cópias | 1 (núcleo) + lembrete curto na liquidação |
| Código Python dentro da pericia-diligencia | ~2.100 tokens | 0 (movido para `scripts/`) |

O ganho maior vem das mudanças de comportamento, que não aparecem na tabela:

- **Busca no projeto uma vez por chat**, e não a cada resposta (pericia-laudo, avaliacao-nr16,
  liquidacao-calculo).
- **Sem encadeamento automático**: nenhuma skill carrega outra por conta própria. Ao fim de
  cada etapa, o Claude oferece em uma linha "gerar DOCX?" ou "revisar?".
- **Revisão responde só com os reprovados**, ou apenas "APROVADO".
- **Esclarecimentos não releem o laudo inteiro**, só as seções impugnadas.
- **Precedente escolhido uma vez por processo**, com a tabela de casamentos conhecidos
  dispensando a busca nos casos comuns. O CSV é filtrado por script, sem entrar inteiro no chat.
- **PDF escaneado**: só as páginas necessárias, a 150 dpi, subindo apenas se ficar ilegível.
- **Descrições exclusivas**: a pericia-laudo deixou de ativar para oitiva, quesitos e NR 16.

Nenhuma regra de conteúdo, fórmula consagrada ou bloco literal foi removido. As regras
repetidas passaram para a **pericia-nucleo**.

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
3. **"(Grifo meu)"**: a pericia-laudo proibia em qualquer reprodução normativa, e a
   pericia-pre-laudo descrevia como formatá-lo em laudo de periculosidade. Ficou assim:
   **proibido em insalubridade e permitido em periculosidade**. Se for proibido sempre, basta
   apagar o parágrafo na pré-laudo.
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

Caminho: Configurações → Capacidades → Skills. Edite a skill ou envie de novo como .zip da
pasta.

Sugestão: guarde uma cópia das versões atuais antes de trocar, para comparar se algo sair
diferente nos primeiros laudos.

## Instruções do Projeto

Se as instruções do seu Projeto repetem regras de redação (travessão, Reclamante, s.m.j.,
frases proibidas), apague-as de lá: agora elas estão na pericia-nucleo. Nas instruções do
Projeto fica só o que não é regra de skill. Se quiser, cole aqui as instruções do Projeto que
eu enxugo.
