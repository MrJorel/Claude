# Roteiro: Webhook Zouti → Planilha KPI com TRAFEGO/ORGANICO

Guia completo para configurar o sistema de captura automática de vendas da Zouti em uma planilha Google Sheets com separação entre tráfego pago e orgânico. Baseado na implementação do MAT10 (Imersão Mestres da Audiência Trabalhista | 10ª Edição).

---

## Visão geral do sistema

```
Zouti (venda confirmada)
    ↓ webhook POST
Apps Script (doPost)
    ↓ grava linha
Aba Vendas (banco de dados)
    ↓ SUMPRODUCT
Aba KPI (dashboard)
```

Cada venda PAID na Zouti dispara um webhook para um Apps Script vinculado à planilha. O script classifica a venda como TRAFEGO ou ORGANICO com base no offer ID, grava uma linha na aba Vendas, e as fórmulas SUMPRODUCT da aba KPI puxam os dados automaticamente por data e source.

---

## Parte 1 — Estrutura da aba Vendas

### Colunas (A até O, 15 no total)

| Col | Nome | Descrição |
|-----|------|-----------|
| A | timestamp | `dd/MM/yyyy HH:mm:ss` (fuso America/Sao_Paulo) |
| B | date | `dd/MM/yyyy` — usada pelas fórmulas SUMPRODUCT |
| C | order_id | ID do pedido Zouti (`ord_xxx`) — usado para deduplicação |
| D | main_qty | Quantidade do produto principal (ingresso) |
| E | ob1_qty | Quantidade do orderbump 1 (ex: gravação/conteúdo) |
| F | ob2_qty | Quantidade do orderbump 2 (ex: material complementar) |
| G | main_net | Valor líquido proporcional do produto principal |
| H | ob1_net | Valor líquido proporcional do ob1 |
| I | ob2_net | Valor líquido proporcional do ob2 |
| J | payment_method | PIX / CREDIT_CARD |
| K | nome | Nome do cliente |
| L | email | Email do cliente |
| M | whatsapp | Telefone (número sem +, ex: 5511999999999) |
| N | source | `TRAFEGO` ou `ORGANICO` |
| O | offerName | Nome legível da oferta (ex: `[MAT10] Tráfego Pago`) |

### Header exato da linha 1:
```
timestamp | date | order_id | main_qty | ob1_qty | ob2_qty | main_net | ob1_net | ob2_net | payment_method | nome | email | whatsapp | source | offerName
```

### Regra de cálculo do valor líquido proporcional

Quando um pedido tem múltiplos itens (ex: ingresso + orderbump), o `net_amount_in_brl` do pagamento é distribuído proporcionalmente pelo bruto de cada item:

```
itemNet = (itemBruto / totalBruto) * netTotal
```

---

## Parte 2 — Classificação TRAFEGO vs ORGANICO

A classificação é feita com base no **offer ID** da Zouti, não no produto.

### Regra geral
- **TRAFEGO**: oferta de tráfego pago (ex: `[PRODUTO] Tráfego Pago`, upsell, orderbump de campanha paga)
- **ORGANICO**: tudo o mais (fluxo de recuperação, recompra, orgânico, lives, checkin, etc.)

### Exemplo MAT10
```javascript
var TRAFEGO_OFFERS = [
  'prod_offer_yw04qnouzs8dm2pemin978',  // [MAT10] Tráfego Pago
  'prod_offer_y5g3g34848bk24fmk5oivl',  // [MAT10] Orderbump (tráfego)
  'prod_offer_z41nafvukg046h1gpm15cw'   // [MAT10] Página de Upsell (tráfego)
];
```

### Produtos vendidos separadamente (ex: gravação/ob1)
Se o ob1 pode ser comprado standalone (não só como orderbump), ele terá **offer IDs próprios** na Zouti. Esses offers precisam entrar no mapa:
- Se a oferta standalone for de upsell/tráfego → entra em `TRAFEGO_OFFERS`
- Se for orgânica (lives, fluxo, recompra) → fica como ORGANICO (padrão)

O script identifica o produto pelo **nome exato** no campo `items[i].name`. Mesmo sendo ob1 standalone, se o nome bater com `PRODUCTS.ob1`, cai na coluna E (ob1_qty) e H (ob1_net).

---

## Parte 3 — Apps Script (doPost)

Cole no Apps Script da planilha e faça o deploy como Web App (acesso: qualquer pessoa).

```javascript
function doPost(e) {
  var orderId = 'desconhecido';
  var logStatus = 'ERRO';
  var logDetalhe = '';
  var logSheet = null;
  var SS_ID = 'ID_DA_PLANILHA_AQUI';

  try {
    Logger.log('Payload: ' + e.postData.contents);
    var ss = SpreadsheetApp.openById(SS_ID);
    logSheet = ss.getSheetByName('Logs');
    var raw = JSON.parse(e.postData.contents);
    var order = raw.data || raw.order || raw;
    orderId = order.id || 'desconhecido';

    if (order.status !== 'PAID') {
      logStatus = 'IGNORADO'; logDetalhe = 'status: ' + order.status;
      return respond({ status: 'ignored', reason: 'not PAID' });
    }

    // ── CONFIGURAR POR PRODUTO ──────────────────────────────────────────
    var PRODUCTS = {
      main: 'Nome exato do produto principal na Zouti',
      ob1:  'Nome exato do ob1 na Zouti',
      ob2:  'Nome exato do ob2 na Zouti'
    };

    var TRAFEGO_OFFERS = [
      'prod_offer_XXXX'  // offer IDs que são tráfego pago
    ];

    var OFFER_NAMES = {
      'prod_offer_XXXX': '[PRODUTO] Tráfego Pago',
      'prod_offer_YYYY': '[PRODUTO] Orgânico - Lives'
      // adicionar todos os offer IDs do produto
    };
    // ────────────────────────────────────────────────────────────────────

    var items = order.items || [];

    // A Zouti manda o offer ID no campo product_offer_id (não offer.id nem offer_id)
    // Fallback completo para cobrir variações do payload entre versões da Zouti
    var offerId = (order.offer && order.offer.id)
               || order.offer_id
               || order.product_offer_id
               || (items[0] && (
                    (items[0].offer && items[0].offer.id)
                    || items[0].offer_id
                    || items[0].product_offer_id
                  ))
               || (raw.offer && raw.offer.id)
               || raw.offer_id
               || raw.product_offer_id
               || '';

    var source = (TRAFEGO_OFFERS.indexOf(offerId) !== -1) ? 'TRAFEGO' : 'ORGANICO';
    var offerName = OFFER_NAMES[offerId] || offerId;

    var payment = order.payment || {};
    var netTotal = payment.net_amount_in_brl || 0;
    var method = payment.method || '';
    var paidAt = order.paid_at || order.created_at;
    var customer = order.customer || {};
    var dateObj = new Date(paidAt);
    var dateStr = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy');
    var timestamp = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');

    var totalBruto = 0;
    for (var i = 0; i < items.length; i++) { totalBruto += items[i].amount_in_brl || 0; }

    var qty = { main: 0, ob1: 0, ob2: 0 };
    var net = { main: 0, ob1: 0, ob2: 0 };

    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var name = (item.name || '').trim();
      var itemBruto = item.amount_in_brl || 0;
      var itemNet = totalBruto > 0 ? (itemBruto / totalBruto) * netTotal : 0;
      for (var key in PRODUCTS) {
        if (name.toLowerCase() === PRODUCTS[key].toLowerCase()) {
          qty[key] += item.quantity || 1; net[key] += itemNet; break;
        }
      }
    }

    if (qty.main === 0 && qty.ob1 === 0 && qty.ob2 === 0) {
      logStatus = 'IGNORADO'; logDetalhe = 'nenhum produto reconhecido';
      return respond({ status: 'ignored', reason: 'no matching products' });
    }

    // Deduplicação por order_id
    var sheet = ss.getSheetByName('Vendas');
    var lastRow = sheet.getLastRow();
    if (lastRow > 1) {
      var existing = sheet.getRange('C2:C' + lastRow).getValues();
      for (var i = 0; i < existing.length; i++) {
        if (existing[i][0] === orderId) {
          logStatus = 'IGNORADO'; logDetalhe = 'duplicata';
          return respond({ status: 'ignored', reason: 'duplicate order_id' });
        }
      }
    }

    var row = [timestamp, dateStr, orderId, qty.main, qty.ob1, qty.ob2,
               round2(net.main), round2(net.ob1), round2(net.ob2),
               method, customer.name || '', customer.email || '', customer.phone || '',
               source, offerName];

    // Retry 3x com 2s de intervalo
    var gravou = false; var erroMsg = '';
    for (var t = 1; t <= 3; t++) {
      try { sheet.appendRow(row); gravou = true; break; }
      catch (eg) { erroMsg = eg.message; if (t < 3) Utilities.sleep(2000); }
    }

    if (gravou) {
      logStatus = 'OK'; logDetalhe = 'source=' + source + ' oferta=' + offerName + ' gravado em ' + dateStr;
      return respond({ status: 'ok', date: dateStr, order_id: orderId, source: source });
    } else {
      logStatus = 'ERRO'; logDetalhe = erroMsg;
      return respond({ status: 'error', message: erroMsg });
    }

  } catch (err) {
    logStatus = 'ERRO'; logDetalhe = err.message;
    Logger.log('ERRO: ' + err.toString());
    return respond({ status: 'error', message: err.message });
  } finally {
    try {
      if (!logSheet) logSheet = SpreadsheetApp.openById(SS_ID).getSheetByName('Logs');
      var ts = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
      logSheet.appendRow([ts, orderId, logStatus, logDetalhe]);
    } catch (le) { Logger.log('Erro no log: ' + le.toString()); }
  }
}

function round2(n) { return Math.round(n * 100) / 100; }
function respond(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }
```

### Deploy
1. Apps Script → Implantar → Nova implantação
2. Tipo: Web app
3. Executar como: Eu
4. Acesso: Qualquer pessoa
5. Copiar a URL gerada e colar no campo de webhook da Zouti

### Teste
- **Não usar o botão "Executar"** — ele não tem payload e vai dar `TypeError: Cannot read properties of undefined (reading 'postData')`. Esse erro é normal e esperado.
- Para testar: usar "Reenviar webhook" em um pedido real na Zouti, ou aguardar a próxima venda.

---

## Parte 4 — Fórmulas SUMPRODUCT na aba KPI

### Lógica das fórmulas
A aba KPI tem uma linha por data (coluna D em diante). Os cabeçalhos de data ficam na **linha 8** (formato `DD/MM`, ex: `23/06`). As fórmulas filtram a aba Vendas por data e source.

### Fórmula padrão — ingresso TRAFEGO por dia
```
=SUMPRODUCT(
  (TEXT(Vendas!$B$2:$B$5029;"DD/MM")=TEXT(D$8;"DD/MM"))
  *(Vendas!$N$2:$N$5029="TRAFEGO")
  *Vendas!$D$2:$D$5029
)
```

### Variações por linha
| O que mede | Coluna Vendas | Filtro N |
|------------|--------------|----------|
| Ingresso TRAFEGO | D (main_qty) | "TRAFEGO" |
| Ingresso ORGANICO | D (main_qty) | "ORGANICO" |
| OB1 TRAFEGO | E (ob1_qty) | "TRAFEGO" |
| OB1 ORGANICO | E (ob1_qty) | "ORGANICO" |
| OB2 TRAFEGO | F (ob2_qty) | "TRAFEGO" |
| Faturamento main TRAFEGO | G (main_net) | "TRAFEGO" |
| Faturamento ob1 ORGANICO | H (ob1_net) | "ORGANICO" |

### Acumulado (coluna C)
```
=SUM(D26:AP26)
```

### Importante
- As datas na coluna B do Vendas podem ser strings (`"23/06/2026"`) ou seriais — o `TEXT(...;"DD/MM")` funciona nos dois casos no Sheets pt_BR.
- Os cabeçalhos de data na linha 8 do KPI são strings curtas (`"23/06"`) — o `TEXT("23/06";"DD/MM")` retorna `"23/06"` e a comparação fecha.
- **Nunca hardcodar valores de venda na linha** — sempre fórmula. Hardcode misturado com SUMPRODUCT duplica contagem.

---

## Parte 5 — Preenchimento retroativo (quando o webhook não existia)

Quando o webhook não estava rodando no início da campanha, é necessário preencher a aba Vendas manualmente com os dados exportados da Zouti.

### Processo
1. Extrair o "Relatório de Pedidos" da Zouti (exportar como Google Sheets)
2. Filtrar apenas pedidos com `Status do Pagamento = PAID`
3. Ignorar PENDING e DECLINED
4. Para cada pedido PAID, montar a linha completa de 15 colunas
5. Ordenar cronologicamente (mais antigo primeiro)
6. Usar `values_append` na API do Sheets ou colar diretamente

### Colunas do export Zouti → colunas do Vendas

| Export Zouti | Coluna Vendas | Observação |
|---|---|---|
| Data de Criação | A (timestamp) e B (date) | Converter para `dd/MM/yyyy HH:mm:ss` e `dd/MM/yyyy` |
| ID | C (order_id) | |
| Produtos | D/E/F (qty) | Identificar qual produto pelo nome |
| Valor Líquido | G/H/I (net) | Proporcional se múltiplos produtos |
| Método de Pagamento | J | |
| Nome do Cliente | K | |
| Email do Cliente | L | |
| Telefone do Cliente | M | |
| ID da Oferta | → N e O | Lookup no mapa TRAFEGO_OFFERS e OFFER_NAMES |

### Deduplicação
- Antes de inserir retroativamente, verificar se a coluna B (date) já cobre as datas do Vendas existente
- Se os dados existentes são de outro produto (ex: MAT09 numa planilha compartilhada), simplesmente acrescentar após a última linha — não há conflito
- Se houver dados do mesmo produto já capturados pelo webhook: verificar order_ids para não duplicar

---

## Parte 6 — Correção de registros incorretos

### Situação: webhook gravou com source errado
Pode acontecer se o script tinha bug no offer ID (ex: typo no ID) ou se a extração do offerId falhava.

**Sintoma no log**: `source=ORGANICO oferta=` (oferta vazia indica que o offerId não foi encontrado)

**Diagnóstico**: checar a aba Logs — se `oferta=` está vazio, o `offerId` estava chegando como string vazia.

**Causa confirmada no MAT10 (jun/2026)**: a Zouti manda o offer ID no campo **`product_offer_id`**, não em `offer.id` nem `offer_id`. O payload não tem nenhuma chave `offer` — elas retornam `null`. O campo correto existe tanto em `order.product_offer_id` quanto em `items[0].product_offer_id`.

**Como diagnosticar**: se o log mostrar `oferta=` vazio, adicionar temporariamente esse bloco logo após extrair o `offerId` vazio:
```javascript
if (!offerId) {
  var diag = 'DIAG: raw_keys=[' + Object.keys(raw).join(',') + ']'
           + ' items0_keys=[' + (items[0] ? Object.keys(items[0]).join(',') : 'sem_items') + ']';
  logDetalhe = diag;
}
```
O log vai mostrar todos os campos disponíveis no payload real — localizar onde está o offer ID e atualizar o fallback.

**Fallback completo (usar sempre)**:
```javascript
var offerId = (order.offer && order.offer.id)
           || order.offer_id
           || order.product_offer_id
           || (items[0] && (
                (items[0].offer && items[0].offer.id)
                || items[0].offer_id
                || items[0].product_offer_id
              ))
           || (raw.offer && raw.offer.id)
           || raw.offer_id
           || raw.product_offer_id
           || '';
```

**Correção em lote**: se N é ORGANICO e deveria ser TRAFEGO, atualizar N e O via `values_update` nas linhas afetadas.

---

## Parte 7 — Checklist de setup para um novo produto

- [ ] Identificar o ID da planilha Google Sheets
- [ ] Criar (ou confirmar existência de) abas: **Vendas**, **Logs**
- [ ] Configurar header do Vendas com 15 colunas (A-O)
- [ ] Confirmar nomes exatos dos produtos na Zouti (main, ob1, ob2)
- [ ] Levantar todos os offer IDs do produto na Zouti
- [ ] Classificar cada offer como TRAFEGO ou ORGANICO
  - Incluir offers de ob1/ob2 standalone se existirem
- [ ] Configurar o Apps Script com SS_ID, PRODUCTS, TRAFEGO_OFFERS, OFFER_NAMES
- [ ] Fazer deploy como Web App
- [ ] Colar URL do webhook na Zouti
- [ ] Confirmar que a aba KPI tem fórmulas SUMPRODUCT referenciando Vendas!N para o filtro de source
- [ ] Corrigir qualquer label de ob2 copiado de produto anterior (ex: "Ônus da Prova" vs "Guia do Atendimento")
- [ ] Preencher retroativo com export da Zouti se necessário

---

## Parte 8 — Armadilhas conhecidas

| Problema | Causa | Solução |
|---|---|---|
| `source=ORGANICO oferta=` no log | `offerId` chegando vazio — campo é `product_offer_id`, não `offer_id` | Usar o fallback completo com `product_offer_id` em order, items[0] e raw |
| Erro `Cannot read properties of undefined (reading 'postData')` | Clicou "Executar" no editor do Apps Script | Normal. Testar via "Reenviar webhook" na Zouti |
| Fórmula SUMPRODUCT retorna 0 mesmo com dados no Vendas | Coluna N do Vendas não existe ou está vazia | Adicionar coluna source e preencher |
| KPI mostra contagem errada (ex: 10 em vez de 9) | Célula diária hardcoded sobrepondo fórmula SUMPRODUCT | Remover hardcode — usar só fórmula |
| Venda do ob1 standalone não entra na coluna E | Nome do produto no payload diferente do configurado no PRODUCTS | Comparar nome exato via log do Apps Script |
| Fórmulas SUMPRODUCT do KPI mostram zero mesmo com dados na aba Vendas | Range começa na linha errada (ex: `$B$49` quando os dados estão nas linhas 2-48) | Fazer find-replace via API: substituir `$49:` por `$2:` em toda a aba KPI |
| Datas como texto vs serial no Vendas | USER_ENTERED com locale pt_BR pode gravar como serial ou string | TEXT(B;"DD/MM") funciona nos dois casos |
| Webhook não chega | URL desatualizada após novo deploy | Sempre usar URL da implantação ativa, não do editor |

---

## Referências rápidas

**Planilha MAT10**: `1madR9hf6JDmPC-yKu_VSf5wVTI3c010kq2vpm_cRwrY`
- Aba KPI: `MAT | 10- Julho`
- Linha do ingresso TRAFEGO: linha 26
- Linha do ingresso ORGANICO: linha 62
- Cabeçalhos de data: linha 8

**Planilha IEA03**: `1B6zdEFTOh2yCKMq5EvEAoNL_yMoaEOds5WObf0z6ais`
- Aba KPI nova: `Página4`
- Linha do ingresso TRAFEGO: linha 26
- Linha do ingresso ORGANICO: linha 62
- Cabeçalhos de data: linha 8
