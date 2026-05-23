# Processo de Teste de Criativos — Funil Perpétuo

## Variáveis de referência

Produto: R$ 67,00
Gateway (4%): R$ 2,68
Imposto produto (10%): R$ 6,70
Imposto Meta (12,5% sobre gasto): incluso no cálculo de CPA real
Margem mínima alvo: 20%

CPA teto (máximo para 20% de margem): R$ 39,00
CPA para escalar (ROI 2x): R$ 33,50

---

## Estrutura de budget diário

Bloco provados (criativos validados): R$ 225,00/dia
Bloco testes (4 criativos simultâneos × R$ 40): R$ 160,00/dia
Total Meta por dia: R$ 385,00

Custo real diário com imposto Meta (12,5%): aproximadamente R$ 433,00

---

## Protocolo de teste de criativos

Entrada: 2 novos criativos por dia
Budget por criativo: R$ 40,00/dia
Duração máxima do teste: 4 dias
Gasto máximo por criativo: R$ 160,00

Criativos simultâneos em teste: 4 (2 dias de janela × 2 entradas por dia)

### Árvore de decisão

DIA 1 — R$ 40 investidos
- Qualquer resultado: aguarda Dia 2.

DIA 2 — R$ 80 acumulados
- 0 vendas acumuladas: CORTAR.
- 1 ou mais vendas acumuladas: avançar para Dia 3.

DIA 3 — R$ 120 acumulados
- CPA acumulado acima de R$ 39: CORTAR.
- CPA acumulado entre R$ 33,50 e R$ 39: avançar para Dia 4.
- CPA acumulado igual ou abaixo de R$ 33,50: ESCALAR.

DIA 4 — R$ 160 acumulados
- CPA acumulado acima de R$ 39: CORTAR.
- CPA acumulado entre R$ 33,50 e R$ 39: MANTER (entra no bloco de rodando).
- CPA acumulado igual ou abaixo de R$ 33,50: ESCALAR.

---

## Estados possíveis de um criativo

TESTE
Criativo nos dias 1 a 4 do protocolo acima.
Budget: R$ 40/dia.
Avaliação diária conforme árvore de decisão.

RODANDO
Criativo que completou o teste com CPA entre R$ 33,50 e R$ 39.
Budget: mantido em R$ 40/dia.
Regra: nunca cortar criativo que vende dentro do CPA.
Nunca escalar automaticamente, mas nunca pausar enquanto CPA estiver abaixo de R$ 39.

ESCALADO (PROVADO)
Criativo que atingiu CPA igual ou abaixo de R$ 33,50.
Budget mínimo: R$ 100/dia.
Regra de escala: aumentar no máximo 20% a cada 7 dias se CPA se mantiver abaixo de R$ 33,50.
Budget atual dos provados: AD 13 (R$ 60/dia) + AD 14 (R$ 130/dia) + novos escalados.

CORTADO
Criativo sem vendas em 2 dias, ou com CPA acima de R$ 39 em qualquer ponto.
Pausar imediatamente. Não reativar sem mudança de criativo.

---

## Regras dos criativos provados

Escalar: apenas se CPA da semana estiver abaixo de R$ 33,50. Aumentar no máximo 20% de uma vez.
Manter: se CPA estiver entre R$ 33,50 e R$ 39. Não mexer no budget.
Cortar: se CPA fechar a semana acima de R$ 39. Pausar sem exceção.

Regra do 3x: se qualquer criativo gastar 3× o CPA alvo (R$ 120) sem nenhuma venda, pausar imediatamente.

---

## Pior cenário diário (todos os testes falham)

Gasto em testes com zero vendas: R$ 160,00 (Meta) + R$ 20,00 (imposto) = R$ 180,00 perdidos.

Para cobrir essa perda e ainda ter lucro, os criativos provados precisam gerar:
- Break-even: 7 vendas/dia.
- 20% de margem mesmo no pior caso: 9 vendas/dia.

Expectativa atual dos provados com R$ 225/dia e CPV médio de R$ 25: aproximadamente 9 vendas/dia.

---

## Checklist diário (humano ou agente)

1. Verificar CPA acumulado de cada criativo em teste.
2. Aplicar a árvore de decisão: cortar, manter, escalar ou avançar de dia.
3. Inserir os 2 novos criativos do dia com R$ 40 cada.
4. Verificar CPA semanal dos criativos provados.
5. Aplicar regra de escala nos provados se CPA abaixo de R$ 33,50.
6. Pausar qualquer provado que fechar semana acima de R$ 39.
7. Registrar resultado do dia: vendas totais, CPA médio, criativos cortados e escalados.

---

## Referência rápida

| Situação | Ação |
|---|---|
| 0 vendas em 2 dias | CORTA |
| CPA acima de R$ 39 | CORTA |
| CPA entre R$ 33,50 e R$ 39 | MANTÉM |
| CPA igual ou abaixo de R$ 33,50 | ESCALA |
| Criativo gasta 3× CPA sem vender | PAUSA IMEDIATA |
| Provado com CPA subindo acima de R$ 39 na semana | CORTA |
