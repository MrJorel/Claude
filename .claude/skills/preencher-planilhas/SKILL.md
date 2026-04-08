# Skill — Preencher Planilhas de KPIs

Atualiza as planilhas de KPIs com dados do Meta Ads para todos os funis ativos.

---

## Quando usar

Quando o usuário pedir para preencher, atualizar ou registrar os dados das planilhas — "preenche as planilhas", "atualiza os KPIs", "coloca os dados de hoje", etc.

---

## Fluxo obrigatório

1. **Confirmar com o usuário:** quais funis quer preencher e qual data?
2. **Buscar dados** do Meta Ads via `insights.py` para cada campanha dos funis selecionados
3. **Confirmar coluna** lendo a linha 20 da aba correspondente (cabeçalho de datas DD/MM)
4. **Escrever na planilha** via `mcp__google-sheets__values_update`:
   - Linhas 21–25: impressões, cliques no link, page views, checkout, vendas gerenciador
   - Linha 66: gasto em ads

> Vendas reais (linha 26+) vêm da Zouti — preencher manualmente por enquanto.

---

## Funis ativos

### MAT08 — LBR (Mestres da Audiência)
- **Conta Meta:** `act_1260766242389591`
- **Planilha:** `1madR9hf6JDmPC-yKu_VSf5wVTI3c010kq2vpm_cRwrY`
- **Aba atual:** `MAT | 08- Abril` (começa em 16/03 na coluna D)
- **Campanhas ativas:**

| ID | Nome |
|----|------|
| 120239797055290591 | CBO MIX 27/03 |
| 120239283642390591 | CBO MIX 16/03 |
| 120228598831550591 | TESTES 16/03 |
| 120228514352150591 | LaL 3% 16/03 |
| 120227170200140591 | QUENTE 16/03 |

---

### IEA02 — Wizoom Play (Imersão Estética Automotiva)
- **Conta Meta:** `act_131069887395970`
- **Planilha:** `1B6zdEFTOh2yCKMq5EvEAoNL_yMoaEOds5WObf0z6ais`
- **Aba atual:** `IEA | 02 - Abril` (começa em 17/03 na coluna D)
- **Campanhas ativas:**

| ID | Nome |
|----|------|
| 120243646687730319 | IEA 02 - 16/03 |
| 120244420544310319 | IEA 02 - CBO - 30/03 |

---

### LTP01 — Lavagem Técnica Protelim (BM Cera)
- **Conta Meta:** `act_626539150391700`
- **Planilha:** `1EMlDk5Yj0fTcdgdCgCzh6FieDrDoTypG1qQ0U2HiyQk`
- **Aba atual:** `LTP01 - Abril` (começa em 01/04 na coluna D)
- **Campanhas ativas:**

| ID | Nome |
|----|------|
| 120225624774640379 | [Wizoom] PERPÉTUO - LTP 01 - CURSO \| PROTELIM |

---

### LTP02 — Lavagem Técnica Protelim (BM Wizoom)
- **Conta Meta:** `act_131069887395970`
- **Planilha:** `1QH1PwyxReXI_UTFctyf8qPqxtTd7RqauFSa4jc-9_wk`
- **Aba atual:** `LTP02 - Abril` (começa em 01/04 na coluna D)
- **Campanhas ativas:**

| ID | Nome |
|----|------|
| 120243432920090319 | PERPÉTUO - LTP 02 - CURSO - 13/03 |

---

### PPF01 — PPF em Peças Essenciais (BM Cera)
- **Conta Meta:** `act_626539150391700`
- **Planilha:** `1DMNZ-3RO89HmaKVEfRAu6a4hMrQidi5mV1P6lnSiHAM`
- **Aba atual:** `PPF01 - Abril` (começa em 01/04 na coluna D)
- **Campanhas ativas:**

| ID | Nome |
|----|------|
| 120234177464770379 | [Wizoom] PERPÉTUO - PPF 01 - CURSO |

---

## Estrutura das planilhas (todas seguem o mesmo padrão)

| Linha | Métrica |
|-------|---------|
| 20 | Datas DD/MM — referência de coluna |
| 21 | # Impressões |
| 22 | # Cliques no link |
| 23 | # Page Views (Visualização de Página) |
| 24 | # Checkout |
| 25 | # Venda Gerenciador |
| 26 | # Venda Real (preencher manualmente via Zouti) |
| 66 | R$ Gasto em Ads |

---

## Como buscar os dados do Meta Ads

```bash
cd ~/.claude/commands/meta-ads

python3 scripts/insights.py campaign \
  --id ID_DA_CAMPANHA \
  --fields "impressions,clicks,spend,actions" \
  --time-increment 1 \
  --time-range '{"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}'
```

Somar para cada funil:
- `impressions` → impressões
- `link_click` (dentro de `actions`) → cliques no link
- `landing_page_view` (dentro de `actions`) → page views
- `initiate_checkout` (dentro de `actions`) → checkout
- `purchase` (dentro de `actions`) → vendas gerenciador
- `spend` → gasto

---

## Observações

- Dados do dia atual ficam disponíveis com ~1h de atraso. Ideal preencher na manhã seguinte.
- Venda Gerenciador ≠ Venda Real. O gerenciador atribui por janela de clique.
- Quando uma nova campanha for criada, adicionar o ID na lista do funil correspondente acima.
- MAT08 e IEA02 têm histórico desde março — as demais (LTP, PPF) começaram em abril.
