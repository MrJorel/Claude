"""
zouti_sheets.py — Busca vendas e faturamento da Zouti (MAT09 / LBR)

Retorna JSON com os dados para o Claude Code gravar na planilha via MCP.

Uso:
  python3 zouti_sheets.py                        → roda para ontem
  python3 zouti_sheets.py --date 2026-05-22      → data específica
  python3 zouti_sheets.py --explore              → mostra estrutura dos pedidos (debug)
"""

import os, sys, time, json, argparse
from datetime import date, timedelta
from collections import defaultdict

sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

ZOUTI_EMAIL    = os.getenv('ZOUTI_EMAIL')
ZOUTI_PASSWORD = os.getenv('ZOUTI_PASSWORD')
ACCOUNT_ID     = 'acc_xhhpimoyb18g139fen6brn'

# Nomes exatos dos produtos na Zouti — confirmar com --explore se mudar de edição
PRODUCTS = {
    'main': 'Imersão Mestres da Audiência Trabalhista | 9º Edição',
    'ob1':  'Imersão Mestres da Audiência Trabalhista | 9º Edição - Conteúdo em Formato de Aulas',
    'ob2':  'Ônus da Prova',
}

# ── Zouti ─────────────────────────────────────────────────────────────────────

def login(page):
    page.goto('https://dashboard.zouti.com.br/login')
    page.wait_for_load_state('networkidle')
    page.click('text=Sou Produtor')
    time.sleep(1)
    # Passo 1: digitar email (type dispara eventos de teclado que habilitam o botão)
    page.locator('#email').click()
    page.keyboard.type(ZOUTI_EMAIL, delay=50)
    time.sleep(0.5)
    page.wait_for_selector('button[type="submit"]:not([disabled])', timeout=10000)
    page.click('button[type="submit"]')
    # Passo 2: digitar senha
    page.wait_for_selector('#password', timeout=10000)
    time.sleep(0.5)
    page.locator('#password').click()
    page.keyboard.type(ZOUTI_PASSWORD, delay=50)
    time.sleep(0.5)
    page.wait_for_selector('button[type="submit"]:not([disabled])', timeout=10000)
    page.click('button[type="submit"]')
    page.wait_for_selector('button:has-text("Vendas")', timeout=20000)
    time.sleep(1)

def fetch_orders(page, date_str):
    all_orders = []
    current_page = 1

    while True:
        url = (f'https://apiv1.zouti.com.br/v1/accounts/{ACCOUNT_ID}/orders'
               f'?page={current_page}&per_page=100&start_date={date_str}&end_date={date_str}&status=PAID')

        data = page.evaluate(f"""async () => {{
            const r = await fetch('{url}', {{
                credentials: 'include',
                headers: {{
                    'Content-Type': 'application/json',
                    'x-zouti-account': '{ACCOUNT_ID}'
                }}
            }});
            return await r.json();
        }}""")

        if 'object' not in data:
            print(f"[ERRO] API Zouti retornou: {data}", file=sys.stderr)
            break

        meta   = data['object']
        orders = meta.get('data', [])
        all_orders.extend(orders)

        if current_page >= meta.get('total_pages', 1):
            break
        current_page += 1

    return all_orders

def aggregate(orders):
    vendas = defaultdict(int)
    fat    = defaultdict(float)

    for order in orders:
        for product in order.get('products', []):
            name = product.get('name', '').strip()
            for key, expected in PRODUCTS.items():
                if name.lower() == expected.lower():
                    vendas[key] += 1
                    net = (
                        product.get('net_amount')
                        or product.get('net_value')
                        or product.get('amount_net')
                    )
                    if net is None:
                        net = order.get('net_amount') or order.get('net_value') or 0
                    fat[key] += float(net or 0)

    return vendas, fat

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date',    help='Data YYYY-MM-DD (padrão: ontem)')
    parser.add_argument('--explore', action='store_true', help='Mostra estrutura dos pedidos')
    args = parser.parse_args()

    target_date = args.date or (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_context().new_page()

        print(f"Fazendo login na Zouti...", file=sys.stderr)
        login(page)
        page.goto(f'https://dashboard.zouti.com.br/{ACCOUNT_ID}/dashboard/infoproduct/sales/orders')
        time.sleep(2)

        print(f"Buscando pedidos PAID de {target_date}...", file=sys.stderr)
        orders = fetch_orders(page, target_date)
        print(f"{len(orders)} pedido(s) encontrado(s)", file=sys.stderr)

        if args.explore:
            if orders:
                print("\n── Estrutura do primeiro pedido ──", file=sys.stderr)
                print(json.dumps(orders[0], indent=2, ensure_ascii=False), file=sys.stderr)
                print("\n── Todos os produtos (campos de valor) ──", file=sys.stderr)
                seen = set()
                for o in orders:
                    for prod in o.get('products', []):
                        name = prod.get('name', '').strip()
                        if name not in seen:
                            seen.add(name)
                            fields = {k: prod.get(k) for k in
                                      ['name','price','amount','net_amount','net_value','amount_net','total']}
                            print(json.dumps(fields, ensure_ascii=False), file=sys.stderr)
            else:
                print("Nenhum pedido encontrado.", file=sys.stderr)
            browser.close()
            return

        vendas, fat = aggregate(orders)
        browser.close()

    result = {
        'date': target_date,
        'vendas': {k: vendas[k] for k in ['main','ob1','ob2']},
        'faturamento': {k: round(fat[k], 2) for k in ['main','ob1','ob2']},
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
