# Processo Diário — Atualização de KPIs do Gerenciador

Atualizar as planilhas MAT08 (LBR) e IEA02 (Wizoom) com os dados do dia atual do Meta Ads.

---

## Contas e planilhas

| Projeto | Conta Meta | Spreadsheet ID |
|---------|-----------|----------------|
| LBR (MAT08) | act_1260766242389591 | 1madR9hf6JDmPC-yKu_VSf5wVTI3c010kq2vpm_cRwrY |
| Wizoom (IEA02) | act_131069887395970 | 1B6zdEFTOh2yCKMq5EvEAoNL_yMoaEOds5WObf0z6ais |

### Campanhas ativas MAT08 (LBR)
- `120239797055290591` — CBO MIX 27/03
- `120239283642390591` — CBO MIX 16/03
- `120228598831550591` — TESTES 16/03
- `120228514352150591` — LaL 3% 16/03
- `120227170200140591` — QUENTE 16/03

### Campanhas ativas IEA02 (Wizoom)
- `120243646687730319` — IEA 02 - 16/03
- `120244420544310319` — IEA 02 - CBO - 30/03

---

## Mapeamento de linhas nas planilhas

Ambas as planilhas têm a mesma estrutura de linhas:

| Linha | Métrica |
|-------|---------|
| 21 | # Impressões |
| 22 | # Cliques no link |
| 23 | # Page Views (Visualização de Página) |
| 24 | # Checkout |
| 25 | # Venda Gerenciador |
| 66 | R$ Gasto em Ads |

---

## Mapeamento de colunas

- **MAT08**: começa em 16/03 na coluna D. Cada dia = +1 coluna.
- **IEA02**: começa em 17/03 na coluna D. Cada dia = +1 coluna.

Para calcular a coluna de uma data:

**MAT08:** dias desde 16/03 + D → ex: 05/04 = 20 dias depois = coluna X  
**IEA02:** dias desde 17/03 + D → ex: 05/04 = 19 dias depois = coluna W

Ou usar a linha 20 da planilha como referência — ela contém as datas no formato DD/MM.

---

## Passo a passo

### 1. Buscar dados do Meta Ads

Usar o script `insights.py` com `--time-range` para o dia desejado, agregando todas as campanhas de cada conta:

```bash
cd ~/.claude/commands/meta-ads

# MAT08 — todas as 5 campanhas, dia X
python3 scripts/insights.py campaign \
  --id 120239797055290591 \
  --fields "impressions,clicks,spend,actions" \
  --time-increment 1 \
  --time-range '{"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}'
```

Repetir para cada campanha e somar os valores de:
- `impressions`
- `link_click` (dentro de `actions`)
- `landing_page_view` (dentro de `actions`)
- `initiate_checkout` (dentro de `actions`)
- `purchase` (dentro de `actions`)
- `spend`

### 2. Confirmar a coluna correta na planilha

Ler a linha 20 da aba (cabeçalho de datas) para confirmar qual coluna corresponde ao dia:

```
mcp__google-sheets__values_get
  range: "MAT | 08- Abril!D20:AQ20"
```

Contar a posição da data alvo → essa é a coluna a preencher.

### 3. Escrever na planilha

Usar `mcp__google-sheets__values_update` para escrever os 5 valores de uma vez (linhas 21–25) e depois o gasto (linha 66):

```
range: "MAT | 08- Abril!X21:X25"
values: [[impressoes], [cliques], [page_views], [checkout], [vendas_ger]]

range: "MAT | 08- Abril!X66"
values: [[gasto]]
```

Repetir para IEA02 na planilha da Wizoom.

---

## Exemplo — 05/04/2026

### MAT08 (LBR) — coluna X
| Métrica | Valor |
|---------|-------|
| Impressões | 39.045 |
| Cliques no link | 264 |
| Page Views | 236 |
| Checkout | 53 |
| Vendas Gerenciador | 16 |
| Gasto em Ads | R$ 793,92 |

### IEA02 (Wizoom) — coluna W
| Métrica | Valor |
|---------|-------|
| Impressões | 14.349 |
| Cliques no link | 89 |
| Page Views | 80 |
| Checkout | 10 |
| Vendas Gerenciador | 5 |
| Gasto em Ads | R$ 219,88 |

---

## Observações

- Os dados do dia atual ficam disponíveis no gerenciador com ~1h de atraso. O ideal é preencher no dia seguinte de manhã (ou no final do dia corrente).
- Vendas Gerenciador ≠ Vendas Reais. O gerenciador atribui por janela de clique — o número real vem da Zouti.
- O campo "Venda Real" (linha 26) deve vir da Zouti — ainda não automatizado, preencher manualmente por enquanto.
- Quando uma nova campanha for criada com nomenclatura MAT08 ou IEA02, adicionar o ID na lista de campanhas acima.
