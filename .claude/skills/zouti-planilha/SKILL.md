---
name: zouti-planilha
description: >
  Configura a automação completa Zouti → Google Sheets via Apps Script.
  Toda vez que uma venda é aprovada na Zouti, o script grava automaticamente uma linha na aba de dados da planilha.
  Suporta múltiplos produtos (main + OBs), múltiplos funis (roteamento por product_offer_id) e registro de comprador (nome, email, whatsapp).
  Use quando o usuário pedir "conectar Zouti com planilha", "automatizar vendas na planilha", "webhook Zouti Google Sheets", ou chamar /zouti-planilha.
  Documentação completa: docs/zouti-planilha-passo-a-passo.md
---

# /zouti-planilha — Automação Zouti → Google Sheets

## O que essa skill faz

Configura o fluxo completo:
```
Zouti (venda aprovada) → webhook HTTP POST → Google Apps Script → aba "Vendas" da planilha
```

Uma linha por pedido. Sem intervenção manual. A planilha atualiza em segundos após cada venda.

---

## Insumos necessários (coletar antes de começar)

1. **ID da planilha** — aparece na URL: `docs.google.com/spreadsheets/d/[ID_AQUI]/edit`
2. **Nome da aba de dados** — geralmente "Vendas" ou "Compradores"
3. **Nome exato do produto principal** — copiar diretamente do painel da Zouti (atenção a espaços, acentos, maiúsculas)
4. **Nomes dos order bumps** — se existirem (OB1, OB2)
5. **Roteamento por oferta?** — se o mesmo produto tem múltiplos funis, pedir os `product_offer_id` de cada oferta e a planilha correspondente a cada um

Se algum estiver faltando, solicitar antes de gerar o código.

---

## Etapas de configuração

### Etapa 1 — Preparar a planilha

Criar aba com nome exato acordado. Linha 1 = cabeçalho:

```
A: timestamp | B: date | C: order_id | D: main_qty | E: ob1_qty | F: ob2_qty
G: main_net | H: ob1_net | I: ob2_net | J: payment_method | K: nome | L: email | M: whatsapp
```

### Etapa 2 — Gerar o código Apps Script

Usar o template abaixo, preenchendo os valores do projeto.

**Template base (projeto simples, sem roteamento por oferta):**

```javascript
function doPost(e) {
  try {
    var raw = JSON.parse(e.postData.contents);
    var order = raw.data || raw.order || raw;
    if (order.status !== 'PAID') {
      return respond({ status: 'ignored', reason: 'not PAID' });
    }
    var PRODUCTS = {
      main: '[NOME_EXATO_PRODUTO_PRINCIPAL]',
      ob1:  '[NOME_EXATO_OB1]',   // remover esta linha se não houver OB1
      ob2:  '[NOME_EXATO_OB2]'    // remover esta linha se não houver OB2
    };
    var items = order.items || [];
    var totalBruto = order.amount_total_in_brl || 0;
    var netTotal = order.payment.net_amount_in_brl || 0;
    var method = order.payment.method || '';
    var paidAt = order.paid_at || order.created_at;
    var customer = order.customer || {};
    var dateObj = new Date(paidAt);
    var dateStr = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy');
    var timestamp = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
    var qty = { main: 0, ob1: 0, ob2: 0 };
    var net = { main: 0, ob1: 0, ob2: 0 };
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var name = (item.name || '').trim();
      var itemBruto = item.amount_in_brl || 0;
      var itemNet = totalBruto > 0 ? (itemBruto / totalBruto) * netTotal : 0;
      for (var key in PRODUCTS) {
        if (name.toLowerCase() === PRODUCTS[key].toLowerCase()) {
          qty[key] += item.quantity || 1;
          net[key] += itemNet;
          break;
        }
      }
    }
    if (qty.main === 0 && qty.ob1 === 0 && qty.ob2 === 0) {
      return respond({ status: 'ignored', reason: 'no [NOME_PROJETO] products' });
    }
    var ss = SpreadsheetApp.openById('[ID_PLANILHA]');
    var sheet = ss.getSheetByName('[NOME_ABA]');
    sheet.appendRow([
      timestamp, dateStr, order.id,
      qty.main, qty.ob1, qty.ob2,
      round2(net.main), round2(net.ob1), round2(net.ob2),
      method,
      customer.name || '', customer.email || '', customer.phone || ''
    ]);
    return respond({ status: 'ok', date: dateStr, order_id: order.id });
  } catch (err) {
    return respond({ status: 'error', message: err.message });
  }
}

function testar() {
  var ss = SpreadsheetApp.openById('[ID_PLANILHA]');
  var sheet = ss.getSheetByName('[NOME_ABA]');
  sheet.appendRow(['TESTE', 'TESTE', 'TESTE', 0, 0, 0, 0, 0, 0, 'TESTE', 'TESTE', 'TESTE', 'TESTE']);
  Logger.log('OK');
}

function round2(n) { return Math.round(n * 100) / 100; }
function respond(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
```

**Template com roteamento por oferta (múltiplos funis, mesmo produto):**

```javascript
function doPost(e) {
  try {
    var raw = JSON.parse(e.postData.contents);
    var order = raw.data || raw.order || raw;
    if (order.status !== 'PAID') {
      return respond({ status: 'ignored', reason: 'not PAID' });
    }
    var offerId = order.product_offer_id || '';
    var SHEETS = {
      '[ID_PLANILHA_FUNIL1]': ['[OFFER_ID_FUNIL1_A]'],
      '[ID_PLANILHA_FUNIL2]': ['[OFFER_ID_FUNIL2_A]', '[OFFER_ID_FUNIL2_B]']
    };
    var spreadsheetId = null;
    for (var ssId in SHEETS) {
      if (SHEETS[ssId].indexOf(offerId) !== -1) {
        spreadsheetId = ssId;
        break;
      }
    }
    if (!spreadsheetId) {
      return respond({ status: 'ignored', reason: 'unknown offer: ' + offerId });
    }
    var PRODUCTS = {
      main: '[NOME_EXATO_PRODUTO_PRINCIPAL]',
      ob1:  '[NOME_EXATO_OB1]'
    };
    var items = order.items || [];
    var totalBruto = order.amount_total_in_brl || 0;
    var netTotal = order.payment.net_amount_in_brl || 0;
    var method = order.payment.method || '';
    var paidAt = order.paid_at || order.created_at;
    var customer = order.customer || {};
    var dateObj = new Date(paidAt);
    var dateStr = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy');
    var timestamp = Utilities.formatDate(dateObj, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
    var qty = { main: 0, ob1: 0, ob2: 0 };
    var net = { main: 0, ob1: 0, ob2: 0 };
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var name = (item.name || '').trim();
      var itemBruto = item.amount_in_brl || 0;
      var itemNet = totalBruto > 0 ? (itemBruto / totalBruto) * netTotal : 0;
      for (var key in PRODUCTS) {
        if (name.toLowerCase() === PRODUCTS[key].toLowerCase()) {
          qty[key] += item.quantity || 1;
          net[key] += itemNet;
          break;
        }
      }
    }
    if (qty.main === 0 && qty.ob1 === 0 && qty.ob2 === 0) {
      return respond({ status: 'ignored', reason: 'no matching products' });
    }
    var ss = SpreadsheetApp.openById(spreadsheetId);
    var sheet = ss.getSheetByName('[NOME_ABA]');
    sheet.appendRow([
      timestamp, dateStr, order.id,
      qty.main, qty.ob1, qty.ob2,
      round2(net.main), round2(net.ob1), round2(net.ob2),
      method,
      customer.name || '', customer.email || '', customer.phone || ''
    ]);
    return respond({ status: 'ok', date: dateStr, order_id: order.id, funnel: spreadsheetId });
  } catch (err) {
    return respond({ status: 'error', message: err.message });
  }
}

function testar() {
  // Substituir pelo ID da planilha de qualquer um dos funis para testar autorização
  var ss = SpreadsheetApp.openById('[ID_PLANILHA_FUNIL1]');
  var sheet = ss.getSheetByName('[NOME_ABA]');
  sheet.appendRow(['TESTE', 'TESTE', 'TESTE', 0, 0, 0, 0, 0, 0, 'TESTE', 'TESTE', 'TESTE', 'TESTE']);
  Logger.log('OK');
}

function round2(n) { return Math.round(n * 100) / 100; }
function respond(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
```

### Etapa 3 — Implantar no Apps Script

1. Acessar script.google.com com a conta Google que tem acesso à planilha
2. Criar novo projeto, colar o código
3. Clicar em "Implantar" → "Nova implantação"
   - Tipo: Aplicativo da Web
   - Executar como: Eu mesmo
   - Quem pode acessar: Qualquer pessoa
4. Copiar a URL que termina em `/exec`

### Etapa 4 — Autorizar acesso à planilha

1. No editor, trocar o dropdown de "doPost" para "testar"
2. Clicar em "Executar"
3. Autorizar o acesso ao Google Sheets quando solicitado
4. Confirmar que apareceu "OK" no log e que a linha "TESTE" apareceu na aba de dados
5. Apagar a linha "TESTE" da planilha

**ATENÇÃO:** Executar "testar" é obrigatório após toda nova implantação. Sem isso, o script não tem permissão para escrever na planilha.

### Etapa 5 — Configurar webhook na Zouti

1. No painel da Zouti: Configurações → Webhooks
2. Criar novo webhook:
   - Nome: qualquer nome identificável
   - URL: a URL do Apps Script (termina em `/exec`)
   - Evento: Pedido Pago
   - Método: POST
3. Salvar e ativar

### Etapa 6 — Validar

1. Usar o botão "Enviar teste" da Zouti — o script vai retornar `{"status":"ignored","reason":"no X products"}` porque o payload de teste usa produtos fictícios. Isso é comportamento correto.
2. Aguardar uma venda real e confirmar que a linha apareceu na aba de dados com os dados corretos.

---

## Fórmulas SUMPRODUCT para aba de KPIs

Após confirmar que as vendas estão gravando, adicionar fórmulas na aba de KPIs para agregar por data:

```
=SUMPRODUCT((TEXT(Vendas!$B$2:$B$5000;"DD/MM")=TEXT(D$8;"DD/MM"))*Vendas!$D$2:$D$5000)
```

Onde:
- `Vendas!$B` = coluna de datas na aba de dados
- `D$8` = célula com a data do cabeçalho da coluna de KPI
- `Vendas!$D` = coluna de valor a somar (trocar conforme a métrica)

Mapeamento coluna → métrica:
- `$D` = main_qty (# vendas produto principal)
- `$E` = ob1_qty (# vendas OB1)
- `$F` = ob2_qty (# vendas OB2)
- `$G` = main_net (faturamento líquido produto principal)
- `$H` = ob1_net (faturamento líquido OB1)
- `$I` = ob2_net (faturamento líquido OB2)

**Atenção:** Separador de argumentos é ponto e vírgula (;) por causa do locale pt_BR.

---

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Linha não aparece na planilha | Script não autorizado | Executar "testar" no editor do Apps Script |
| Linha não aparece na planilha | Nome do produto diferente do cadastrado | Comparar nome na Zouti com o nome no código (espaços, acentos) |
| Linha não aparece na planilha | Nova implantação sem reautorizar | Executar "testar" novamente |
| "Página não encontrada" | Autorização caiu ou URL errada | Verificar URL e executar "testar" |
| Fórmula retorna 0 | Separador errado (vírgula em vez de ;) | Trocar para ponto e vírgula |
| Webhook teste retorna "ignored" | Produto fictício no teste da Zouti | Normal. Aguardar venda real |
| URL do webhook mudou | Nova implantação em vez de editar existente | Editar implantação existente, selecionar "Nova versão" |

---

## Projetos configurados

Ver [docs/zouti-planilha-passo-a-passo.md](../../../docs/zouti-planilha-passo-a-passo.md) — Parte 6 — para os detalhes de cada projeto ativo (IDs de planilha, nomes de produto, offer IDs, URLs de webhook).
