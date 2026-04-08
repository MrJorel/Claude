# Skill — Preencher Planilhas de KPIs

Skill para atualizar as planilhas de KPIs do gerenciador (Meta Ads) para LBR e/ou Wizoom.

---

## Quando usar

Quando o usuário pedir para preencher, atualizar ou registrar os dados das planilhas — seja com "preenche as planilhas", "atualiza os KPIs", "coloca os dados de hoje", etc.

---

## Fluxo obrigatório

### Passo 1 — Ler o processo atualizado

Antes de qualquer coisa, ler:

```
scripts/zouti-sheets/PROCESSO_DIARIO.md
```

Isso garante que campanhas, IDs e estrutura das planilhas estão atualizados.

### Passo 2 — Confirmar com o usuário

Perguntar:

> "Quais projetos você quer preencher hoje? LBR, Wizoom ou os dois? E qual data?"

Aguardar confirmação antes de executar.

### Passo 3 — Executar

Seguir o passo a passo do PROCESSO_DIARIO.md:

1. Buscar dados do Meta Ads via `insights.py` para cada campanha do(s) projeto(s) confirmado(s)
2. Somar: impressões, cliques no link, page views, checkout, vendas gerenciador, gasto
3. Confirmar coluna correta lendo linha 20 da planilha
4. Escrever nas linhas 21–25 (métricas) e 66 (gasto) via `mcp__google-sheets__values_update`

---

## Referência rápida

| Projeto | Conta Meta | Spreadsheet ID |
|---------|-----------|----------------|
| LBR (MAT08) | act_1260766242389591 | 1madR9hf6JDmPC-yKu_VSf5wVTI3c010kq2vpm_cRwrY |
| Wizoom (IEA02) | act_131069887395970 | 1B6zdEFTOh2yCKMq5EvEAoNL_yMoaEOds5WObf0z6ais |

> Campanhas e estrutura detalhada: ver PROCESSO_DIARIO.md (sempre mais atualizado que esta skill).
