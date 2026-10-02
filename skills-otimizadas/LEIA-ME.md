# Skills de perícia reorganizadas: o que mudou e como instalar

Prioridade adotada: **qualidade e precisão primeiro; economia só onde não custa nada.**

## Resultado

| | Antes | Depois |
|---|---:|---:|
| Texto das skills (sempre que a skill é usada) | ~25.000 tokens | ~21.800 tokens |
| Arquivos de consulta por agente (lidos só quando o agente é avaliado) | não existiam | ~6.900 tokens |
| Instruções do Projeto (vão em TODA mensagem) | ~4.000 tokens | ~1.100 tokens |
| Correções de Keverson presentes nas skills | parte | todas as 26 memórias do Projeto |

O texto das skills ficou quase do mesmo tamanho porque agora contém tudo que antes só existia na
memória, recuperado por busca e sem garantia de ser encontrado. A economia vem de outro lugar:
- instruções do Projeto 4x menores (vão em toda mensagem);
- busca completa nos arquivos uma vez por agente em cada chat, não a cada resposta;
- conferências mecânicas feitas por script, sem gastar leitura do Claude.

## Automação (nada depende de Keverson pedir)

| Momento | O que acontece sozinho |
|---|---|
| Processo novo | Escolha do precedente |
| Peça completa pronta | Revisão (estilo + mérito + varredura contra os autos) → correções → DOCX → conferência do arquivo |
| Seção isolada (oitivas, quesitos) | Checagem por script antes de entregar |
| Quesitos | Conferência palavra por palavra contra a peça da parte + conferência de lastro de cada "Vide Laudo" |
| DOCX montado a partir de precedente | Limpeza das imagens órfãs do outro processo |

## Scripts novos (o Claude só executa, não lê)

- `pericia-revisao/scripts/checar.py`: confere travessão, frases proibidas, jargão, "não aferível por
  meios periciais", impossibilidade suspeita, RESPOSTA em caixa alta, NR com hífen, Sr./Sra.
  minúsculo, placeholders, Markdown, pontuação duplicada, OJ 385 com conclusão binária, nome da
  mesma pessoa grafado diferente, meta-comentário que vazou para o texto e, no .docx, fonte fora do
  padrão e imagem órfã de outro processo.
- `pericia-revisao/scripts/limpar_midia.py`: remove do .docx as fotos do precedente que ficam
  escondidas no arquivo.
- `pericia-revisao/scripts/medir_acervo.py`: mede o acervo real e mostra a frequência de cada
  convenção de formatação (resolve dúvidas pela maioria dos laudos, sem alterar nada).
- `pericia-quesitos/scripts/conferir_quesitos.py`: compara cada enunciado transcrito com o PDF da
  parte e aponta palavra trocada, cortada ou "consertada".
- `pericia-diligencia/scripts/`: Resumo para Diligência (agora com suporte a ação coletiva) e Lista
  de Presença XLSX.

## Correções em relação às skills antigas (vieram das memórias)

1. "(Grifo meu)" era proibido; é usado (laudo 210, laudos de periculosidade), com a alínea em
   negrito real.
2. "Pela negativa" era "não usar em insalubridade"; é usado sozinho em quesito fechado.
3. "Diante do exposto" e "corrobora" eram jargão; são estilo seu.
4. Destaque final da conclusão era "sem negrito"; é negrito (laudos 156 a 175, 210, 63).
5. Sr./Sra. sempre maiúsculo (instruções antigas do Projeto diziam minúsculo).
6. Formatação "Arial 12, margens 1440" das instruções antigas; o padrão é Verdana e margens
   1701/2127/1701/1134.
7. Esclarecimentos não têm linhas "Reclamante:/Reclamada:" no cabeçalho.
8. Diligência: só horário de início (regra geral de 29/08/2026).

## Pontos que ainda dependem de Keverson

1. ~~Imagem da lista de presença~~: RESOLVIDO (02/10/2026), imagem após os nomes com a legenda
   "Lista de Presença" abaixo.
2. ~~Impugnação só de advogado~~: RESOLVIDO, registrar a ausência de peça técnica só quando não
   há manifestação de assistente técnico.
3. **Alinhamento dos títulos** (esquerda x justificado) e **marcador nativo em "Acompanharam"**:
   as memórias divergem; como a formatação é herdada do laudo-base, o efeito é pequeno, mas o
   `medir_acervo.py` resolve pela maioria.
4. A memória "Insalubridade e Periculosidade" está vazia (só o título).

## Versão conferida

As datas das skills analisadas coincidem com as da conta (Configurações > Habilidades): diligência
e pré-laudo 03/09, revisão e oitivas 29-30/08, laudo, quesitos, esclarecimentos e manifestação
14/06, precedentes e docx 07/06, liquidação 04/06, avaliacao-nr16 30/05. O `build_resumo.py`
citado na memória nunca foi publicado na skill; o script novo cobre a mesma função (ação coletiva
e "Local de trabalho (dia a dia)").

## Como instalar (depois da conferência acima)

1. Guarde uma cópia das versões atuais (menu ⋮ de cada skill, se houver opção de baixar).
2. Crie a skill `pericia-nucleo`.
3. Substitua pericia-laudo, pericia-revisao, pericia-quesitos, pericia-esclarecimentos,
   pericia-manifestacao, pericia-oitivas, pericia-pre-laudo, pericia-diligencia,
   pericia-precedentes e avaliacao-nr16 pelos pacotes novos (com as pastas scripts/ e
   references/).
4. pericia-docx e liquidacao-calculo: manter as instaladas (têm seus scripts e dados).
5. Troque as instruções do Projeto pelo texto de `instrucoes-projeto/INSTRUCOES-PROPOSTAS.md`.
6. Teste com um processo já concluído e compare com o protocolado.
7. Só depois, e com calma, enxugue a memória do Projeto: tudo dela está nas skills, mas mantenha-a
   até o teste confirmar.
