# Conectar Zouti com Google Sheets via Apps Script
## Guia completo, passo a passo, à prova de falha

---

## O que esse sistema faz

Toda vez que uma venda é aprovada na Zouti, o sistema:
1. Recebe o webhook automático da Zouti
2. Identifica qual produto foi vendido (produto principal, OB1, OB2)
3. Grava uma linha na aba "Vendas" da planilha correta
4. As fórmulas na aba de KPIs atualizam automaticamente

Não tem intervalo de tempo. Não precisa rodar nada manualmente. A planilha atualiza em segundos após cada venda.

---

## Arquitetura

```
Zouti (venda aprovada)
    ↓ webhook automático (HTTP POST com JSON)
Google Apps Script (URL pública)
    ↓ grava linha
Aba "Vendas" da planilha
    ↓ fórmulas SUMPRODUCT
Aba de KPIs (linhas de quantidade e faturamento por dia)
```

---

## Parte 1: Preparar a planilha

### 1.1 Criar a aba "Vendas"

Na planilha de KPIs do projeto, crie uma aba chamada exatamente "Vendas" (ou "Compradores" se o projeto já usa esse nome).

### 1.2 Configurar o cabeçalho

Na linha 1 da aba Vendas, coloque exatamente essas colunas nessa ordem:

```
A: timestamp
B: date
C: order_id
D: main_qty
E: ob1_qty
F: ob2_qty
G: main_net
H: ob1_net
I: ob2_net
J: payment_method
K: nome
L: email
M: whatsapp
```

Cada venda vai gerar uma linha com essas informações. Uma linha por pedido.

- main = produto principal
- ob1 = order bump 1
- ob2 = order bump 2
- qty = quantidade vendida
- net = valor líquido (já descontada a taxa da Zouti)

### 1.3 Criar as fórmulas na aba de KPIs

Na aba de KPIs (ex: "MAT | 09- Junho"), as linhas de vendas e faturamento precisam de fórmulas que somam a aba Vendas filtrando pela data da coluna.

A fórmula padrão é:

```
=SUMPRODUCT((TEXT(Vendas!$B$2:$B$5000;"DD/MM")=TEXT(D$8;"DD/MM"))*Vendas!$D$2:$D$5000)
```

Explicando:
- `TEXT(Vendas!$B$2:$B$5000;"DD/MM")` converte as datas da coluna B da aba Vendas para o formato "DD/MM"
- `TEXT(D$8;"DD/MM")` converte a data do cabeçalho da coluna atual para o mesmo formato
- Os dois são comparados para filtrar só as linhas do dia certo
- O resultado é multiplicado pela coluna de valor (ex: $D para main_qty)

ATENÇÃO: O separador de argumentos é ponto e vírgula (;), não vírgula. Isso é por causa do locale pt_BR do Google Sheets.

Mapeamento de colunas da aba Vendas para as linhas de KPI:

| Linha de KPI | Métrica | Coluna da aba Vendas |
|---|---|---|
| # Venda Real Produto Principal | main_qty | $D |
| # Venda Real OB1 | ob1_qty | $E |
| # Venda Real OB2 | ob2_qty | $F |
| Faturamento Produto Principal | main_net | $G |
| Faturamento OB1 | ob1_net | $H |
| Faturamento OB2 | ob2_net | $I |

As fórmulas vão nas células das datas onde a automação começa. As datas anteriores podem ser mantidas com valores inseridos manualmente.

---

## Parte 2: Criar o Apps Script

### 2.1 Abrir o Apps Script

Acesse script.google.com com a conta Google que tem acesso à planilha. Clique em "Novo projeto".

### 2.2 Colar o código

Delete o código padrão que aparece e cole o código do projeto (ver seção "Códigos" abaixo). Cada projeto tem um código próprio com os nomes dos produtos e o ID da planilha.

### 2.3 Implantar como aplicativo da web

Clique em "Implantar" (botão azul no topo direito) → "Nova implantação".

Configure assim:
- Tipo: Aplicativo da Web
- Executar como: Eu mesmo (o dono da conta Google)
- Quem pode acessar: Qualquer pessoa

Clique em "Implantar". O Google vai pedir autorização. Clique em "Autorizar acesso" e confirme com a conta Google. Copie a URL gerada — ela termina em `/exec`.

### 2.4 Autorizar o acesso à planilha

Mesmo após implantar, o script precisa de autorização para escrever na planilha. Para isso:

1. No editor do Apps Script, troque a função no dropdown de "doPost" para "testar"
2. Clique em "Executar"
3. O Google vai pedir permissão para acessar o Google Sheets. Clique em "Revisar permissões" e autorize

Se o "testar" rodar com sucesso, aparece "OK" no log e uma linha "TESTE" vai aparecer na aba Vendas da planilha. Isso confirma que a autorização foi concedida.

ATENÇÃO IMPORTANTE: Se você implantar uma nova versão do código sem executar o "testar" novamente, o script pode quebrar. Sempre execute "testar" após qualquer nova implantação.

### 2.5 Atualizar o código sem mudar a URL

Se precisar corrigir o código depois, o processo é:
1. Edite o código no editor
2. Clique em "Implantar" → "Gerenciar implantações"
3. Clique no ícone de lápis (editar) da implantação existente
4. Em "Versão", selecione "Nova versão"
5. Clique em "Implantar"
6. Execute "testar" de novo para reautorizar

Isso mantém a mesma URL. Se criar uma nova implantação em vez de editar a existente, a URL muda e você precisa atualizar no webhook da Zouti.

---

## Parte 3: Configurar o webhook na Zouti

### 3.1 Acessar webhooks

No painel da Zouti, vá em Configurações → Webhooks (ou Integrações → Webhooks, dependendo da versão).

### 3.2 Criar o webhook

- Nome: qualquer nome identificável (ex: "Planilha MAT09")
- URL: a URL do Apps Script (a que termina em `/exec`)
- Evento: Pedido Pago (ou equivalente — é o evento que dispara quando status muda para PAID)
- Método: POST

Salve.

### 3.3 Testar o webhook

A Zouti tem um botão de "Enviar teste" ou "Test webhook". Ao clicar, ela envia um payload com dados fictícios para a URL. O script vai receber, mas como o nome do produto fictício não bate com os produtos cadastrados no script, ele vai retornar `{"status":"ignored","reason":"no [projeto] products"}` — isso é o comportamento correto.

O verdadeiro teste é uma venda real. Quando cair, verifica a aba Vendas.

---

## Parte 4: Como o script funciona por dentro

### 4.1 Estrutura do payload da Zouti

Quando uma venda é aprovada, a Zouti envia um JSON com essa estrutura:

```json
{
  "id": "ord_xxxx",
  "status": "PAID",
  "product_offer_id": "prod_offer_xxxx",
  "amount_total_in_brl": 97,
  "paid_at": "2026-05-25T14:00:00.000Z",
  "items": [
    {
      "name": "Nome exato do produto",
      "amount_in_brl": 97,
      "quantity": 1
    }
  ],
  "payment": {
    "method": "PIX",
    "net_amount_in_brl": 63.82
  },
  "customer": {
    "name": "Nome do comprador",
    "email": "email@exemplo.com",
    "phone": "5511999999999"
  }
}
```

### 4.2 O que o script faz com o payload

1. Verifica se `status === "PAID"`. Se não for, ignora.
2. Identifica os produtos comprando o `items[].name` com a lista de produtos configurados no script
3. Calcula o valor líquido de cada item proporcionalmente: `(item.amount_in_brl / total_bruto) * net_total`
4. Grava uma linha na aba Vendas com timestamp, data, order_id, quantidades, valores líquidos, método e dados do comprador
5. Retorna `{"status":"ok"}` para a Zouti

### 4.3 Roteamento por oferta (quando há múltiplos funis)

Quando o mesmo produto tem duas ou mais ofertas distintas (ex: uma oferta para cada gestor de tráfego), o script usa o campo `product_offer_id` para decidir em qual planilha gravar.

Exemplo: LTP01 e LTP02 vendem o mesmo produto, mas cada oferta tem um `product_offer_id` diferente. O script verifica em qual lista de IDs o `product_offer_id` da venda se encaixa e grava na planilha correspondente.

Se o `product_offer_id` não corresponder a nenhuma lista cadastrada, o script retorna `{"status":"ignored","reason":"unknown offer: [id]"}` e não grava nada.

---

## Parte 5: Problemas comuns e soluções

### Webhook não chega na planilha

Possíveis causas:
1. O script não foi autorizado. Solução: execute "testar" no editor do Apps Script.
2. O nome do produto no script não bate exatamente com o nome na Zouti. Verificar espaços extras, acentos, maiúsculas. O script usa `.trim()` para remover espaços no início/fim, mas diferenças no meio do nome vão falhar.
3. A URL do webhook na Zouti está errada. Verificar se termina em `/exec`.
4. Uma nova versão foi implantada sem executar "testar". A autorização pode ter caído.

### Fórmulas retornam 0

Possíveis causas:
1. A aba Vendas está vazia (ainda não teve vendas). Normal.
2. O separador da fórmula está errado. No Brasil, deve ser ponto e vírgula (;). Exemplo correto: `=SUMPRODUCT((TEXT(A;"DD/MM")=TEXT(B;"DD/MM"))*C)`.
3. A data na coluna B da aba Vendas não está sendo reconhecida como data. O Google Sheets converte automaticamente strings no formato "dd/MM/yyyy" para número serial de data quando inseridas via appendRow. A fórmula usa TEXT() em ambos os lados justamente para lidar com esse formato.

### Script retorna "Página não encontrada"

Isso acontece quando a autorização caiu ou quando o script foi implantado de novo sem reautorizar. Solução: execute "testar" no editor para reautorizar.

### Produto com orderbump: valores líquidos

Quando um pedido tem produto principal + OB, o valor líquido total do pedido é dividido proporcionalmente pelo valor bruto de cada item. Fórmula: `(item.amount_in_brl / order.amount_total_in_brl) * order.payment.net_amount_in_brl`. Isso garante que a soma dos líquidos de cada item sempre bate com o líquido total do pedido.

---

## Parte 6: Códigos por projeto

### MAT09 (LBR)
- Planilha: `1madR9hf6JDmPC-yKu_VSf5wVTI3c010kq2vpm_cRwrY`
- Aba de dados: `Vendas`
- Aba de KPIs: `MAT | 09- Junho`
- Produtos: Imersão Mestres da Audiência Trabalhista | 9º Edição (main), versão Aulas (ob1), Ônus da Prova (ob2)
- Webhook: Zouti conta LBR

### PPF01 (Wizoom)
- Planilha: `1DMNZ-3RO89HmaKVEfRAu6a4hMrQidi5mV1P6lnSiHAM`
- Aba de dados: `Compradores`
- Aba de KPIs: `PPF01 - Maio`
- Produtos: PPF Essencial (main), Como Aplicar PPF em FARÓIS (ob1), Guia do Atendimento Magnético (ob2)
- Webhook: Zouti conta Wizoom

### LTP01 e LTP02 (Wizoom, mesmo script)
- Planilha LTP01: `1EMlDk5Yj0fTcdgdCgCzh6FieDrDoTypG1qQ0U2HiyQk`
- Planilha LTP02: `1QH1PwyxReXI_UTFctyf8qPqxtTd7RqauFSa4jc-9_wk`
- Aba de dados: `Vendas` (em cada planilha)
- Roteamento: pelo `product_offer_id`
  - LTP01: `prod_offer_vz7jn1ijag3znt60kfy4rv`
  - LTP02: `prod_offer_56w3fyxr13tjzjo32kpfp0`, `prod_offer_o1x9iunbqbwfa05fnljxva`, `prod_offer_egaugpeun3j20g47otzh33`
- Produtos: Lavagem Técnica + Lavagem de Motor - Protelim (main), [Acesso Vitalício] versão (ob1)
- Webhook: Zouti conta Wizoom (mesmo webhook do PPF, script diferente)

---

## Parte 7: Manutenção mensal

No início de cada novo mês:
1. Criar a nova aba de KPIs (ex: "MAT | 10- Julho") — geralmente copiando a aba do mês anterior
2. Adicionar as fórmulas SUMPRODUCT nas linhas de venda e faturamento para as colunas do novo mês
3. A aba Vendas é contínua — não precisa criar uma nova por mês. As fórmulas filtram por data então o histórico todo fica acessível
4. Se a aba Vendas passar de 5000 linhas, aumentar o range nas fórmulas (ex: $B$2:$B$10000)

---

## Parte 8: Checklist de configuração para um novo projeto

- [ ] Identificar os nomes exatos dos produtos na Zouti (copiar do painel, com atenção a espaços e acentos)
- [ ] Identificar os `product_offer_id` se houver roteamento por oferta
- [ ] Criar aba Vendas na planilha com o cabeçalho correto
- [ ] Criar o projeto no Apps Script (script.google.com)
- [ ] Colar o código com o ID da planilha e nomes dos produtos corretos
- [ ] Implantar como aplicativo da web (Qualquer pessoa, Executar como: Eu mesmo)
- [ ] Executar "testar" para autorizar o acesso à planilha
- [ ] Confirmar que a linha "TESTE" apareceu na aba Vendas
- [ ] Apagar a linha "TESTE" da aba Vendas
- [ ] Configurar webhook na Zouti com a URL do script
- [ ] Aguardar uma venda real e confirmar que gravou na aba Vendas
- [ ] Adicionar as fórmulas SUMPRODUCT nas linhas de KPI correspondentes
