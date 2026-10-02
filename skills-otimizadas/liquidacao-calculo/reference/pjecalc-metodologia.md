# PJe-Calc: sistema, parâmetros e metodologia

A técnica serve à fidelidade ao título; nunca o amplia.

## Fluxo do Cálculo Externo

Dados do Processo > Parâmetros > Parcelas Atualizáveis (4 abas) > Atualização > Liquidar >
Imprimir > Relatório Consolidado. "Sem recálculo" = usar os números do PJe-Calc como finais.

- Juros SEMPRE em campo separado do principal (misturar gera anatocismo).
- "Data da Última Atualização" = data da liquidação do relatório de origem, NUNCA a data da
  assinatura eletrônica.
- Armadilha do índice: "Índice Trabalhista" é o índice geral; se ficar "Sem Correção",
  honorários e custas CONGELAM.
- SELIC como CORREÇÃO e SELIC como JUROS são portas diferentes (mesma tabela).
- Contribuição social: segurado e patronal em campos separados por período (até fev/2009 = 0,00
  digitado; a partir de mar/2009 = valores); campo com asterisco não aceita vazio.
- Limitação conhecida do Cálculo Externo: consolida segurado + patronal numa só competência e
  roda SELIC sobre o total; diverge da origem quando a cota patronal não tinha juros. Não é
  corrigível: registrar na peça.
- Versão 2.16.0 aplica o desconto simplificado do IRPF; as 2.15.x não.

## Parâmetros e histórico (aprendido em uso)

- Campo Demissão = data do afastamento (fim do aviso trabalhado). Projeção do aviso indenizado:
  campo "Projetar Aviso Prévio Indenizado", nunca pela data de demissão.
- Prazo do Aviso Prévio: "Calculado" quando todo o aviso é indenizado (Lei 12.506, 30 + 3/ano);
  "Informado" com os dias quando parte foi trabalhada e só o excedente foi deferido.
- "Limitar Cálculo / Data Final" em branco quando não há limitação de período; não usar para
  marcar fim de contrato.
- Histórico salarial: "Última Remuneração" em branco (senão cria histórico de valor único);
  cadastrar a evolução real da CTPS. Mês da rescisão sem FGTS e sem Contribuição Social no
  histórico (vêm pela verba saldo; evitar bis in idem), mantendo o valor apenas como base.
- FGTS com extrato juntado: meses depositados como "Recolhido" com os valores do extrato (a
  diferença zera com "Zerar Valor Negativo"), mantidos na base dos 40%; sem extrato, apurar
  integral.

## Correção monetária e juros

- Padrão trifásico (privado, ADC 58): IPCA-E + TRD simples (pré-judicial) > SELIC (do
  ajuizamento) > IPCA + Taxa Legal (a partir de 30/08/2024, art. 406 CC, Lei 14.905/2024).
  Acúmulo a partir do mês subsequente ao vencimento (CLT 459 §1º; Súm. 381 TST). Sempre
  subordinado ao critério fixado na decisão, se houver; se a decisão fixou critério próprio,
  mantê-lo e explicar a transição de 30/08/2024 como regime legal superveniente.
- Ação ajuizada APÓS 30/08/2024: SOMENTE "IPCA e Taxa Legal" para todos os períodos, inclusive o
  pré-judicial; sem SELIC e sem IPCA-E.
- Fazenda Pública (inclusive ECT, se confirmado na sentença): IPCA-E até 30/11/2021 + SELIC a
  partir de 12/2021 (EC 113/2021, art. 3º); não aplicar o regime privado da ADC 58. A EC 113
  prevalece sobre a Lei 14.905/2024 (hierarquia constitucional).
- Na peça, os critérios vão em linha corrida, nunca separando correção e juros em linhas
  distintas.

## Horas extras: multicálculo

- Após a descaracterização do 12x36 (8ª diária/44ª semanal), as HE se dividem em QUATRO verbas:
  HE 50%, HE 100%, HE 50% NOTURNAS e HE 100% NOTURNAS, cada uma com sua quantidade.
- O total do cartão = SOMA das verbas do mesmo eixo, nunca uma só.
- Cenários (mais favorável, extra noturna, primeiras em separado): rodar separados e cruzar;
  NUNCA somar entre eixos.
- O multiplicador noturno JÁ embute o adicional de 20% (OJ 97 SDI-1): 1,5 > 1,8; 2,0 > 2,4.
- "Diferença adicional noturno 20%" autônoma só para horas noturnas normais (sem bis in idem).
- Hora ficta noturna: o sistema já aplica (CLT 73 §1º; Súm. 60): nunca recalcular ÷0,857.

## Fórmulas padrão

HE 50% = sal ÷ 220 x 1,5 x Qt | HE 100% = sal ÷ 220 x 2,0 x Qt | Adicional noturno = sal ÷ 220 x
0,20 x HsNot | Periculosidade = sal-base x 0,30 (Súm. 191) | Insalubridade = SM ou sal-base x grau
| Intrajornada = sal ÷ 220 x 1,5 x HsIntra | Multa 40% = saldo FGTS x 0,40 | ÷1,20 só para extrair
o salário-base de total que já inclui periculosidade.

## FGTS

- "Integralidade" = todo o contrato, inclusive meses com salário pago e FGTS não depositado.
- Extrato do eSocial = fonte mais confiável; DECLARAR não é DEPOSITAR.
- Depósito tardio (após a rescisão) abate o principal mas NÃO elimina a multa de 40% (Tema 68
  IRR/TST); no Resumo, não citar o Tema 68.
- Base da multa 40%: OJ 42 II, "Excluir AP" SEMPRE marcado em todo cálculo; única exceção: ordem
  EXPRESSA em contrário na sentença.
- Unicidade com rescisão fictícia intermediária: DEP RESCISORIO (8% sal) > ocorrência mensal;
  DEP VERBAS IND + DEP MULTA RESCISORIA > Saldo e/ou Saque com Deduzir, somados numa linha, mesma
  data; NUNCA inflar a base mensal para bater com o recolhido.

## Pagamento em juízo (após o ajuizamento)

NÃO lançar na coluna "valor pago" da ocorrência da verba (para os juros desde o vencimento
original, o que favorece a Ré). Lançar na data REAL do pagamento em VERBAS > Expresso > "Valor
pago tributável" / "não tributável" (Livro p. 372 a 374). IRPF = 0: valor único; IRPF > 0:
ratear (saldo/13º = tributável; férias + 1/3, aviso, multas = não tributável).

## IRPF 2026 (tabela progressiva mensal, honorários no PJe-Calc; conferir vigência)

Isento até R$ 2.428,80; faixa máxima a partir de R$ 4.664,69: 27,5% com dedução de R$ 908,73;
desconto simplificado mensal R$ 607,20 (substitui deduções legais quando mais vantajoso);
dependente R$ 189,59. Redutor da Lei 15.270/2025 (a partir de 01/01/2026, art. 6º-A Lei
9.250/95): até R$ 5.000,00, redução de até R$ 312,89 (limitada ao imposto, sem crédito); de
R$ 5.000,01 a R$ 7.350,00, redução = 978,62 - (0,133145 x rendimento); acima de R$ 7.350,00, sem
redutor. Pendente: verificar se a versão instalada do PJe-Calc aplica o redutor na faixa de
R$ 5.000,01 a R$ 7.350,00. "Apurar IR > IRPF" exige o CPF do credor (PJe > Partes e
Representantes, procuração ou nomeação).

## Limitação à inicial

Só com ordem EXPRESSA, e NÃO se aplica quando a inicial ressalva que os valores são estimativa
(IN 41/2018, art. 12). Parâmetro = total de CADA verba sem juros e sem correção. No PJe-Calc:
"compor principal: não" na verba e nos reflexos, verba-referência com o valor da inicial e
comparação após liquidar.

## CSV

Histórico salarial: separador ";" entre aspas; "MES_ANO";"VALOR";"FGTS"; mm/aaaa; vírgula
decimal; CRLF. Cartão de ponto: Data;Entrada1;Saída1;... ("Saída" com acento); dd/mm/aaaa; hh:mm;
sem turno = campos vazios; tempo >= 24h é erro (zerar a linha).

## Extração de PDF

pdfinfo > pdftotext > grep -n de marcadores > sed -n do intervalo. Holerites com rubrica inline:
re.findall(r'(\d{4})\s+([\d]+,[\d]+)').
