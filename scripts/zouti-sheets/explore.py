"""
Testa busca de pedidos aprovados de ontem para LBR e Wizoom
"""
import os, sys, time, json
from datetime import date, timedelta
sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

EMAIL    = os.getenv('ZOUTI_EMAIL')
PASSWORD = os.getenv('ZOUTI_PASSWORD')

ACCOUNTS = {
    'LBR':    'acc_xhhpimoyb18g139fen6brn',
    'Wizoom': 'acc_1idr3k8zzv9480cah4d50z',
}

# Testar com 04/04 (ontem) pra ter dados garantidos
DATE = '2026-04-04'

PRODUCTS_LBR = [
    'Imersão Mestres da Audiência Trabalhista | 8º Edição',
    'Imersão Mestres da Audiência Trabalhista | 8º Edição - Conteúdo em Formato de Aulas',
    'Ônus da Prova',
]
PRODUCTS_WIZOOM = [
    'Imersão Estética Automotiva 30K | 2ª Edição',
    'Imersão Estética Automotiva 30K | 2º Edição - Conteúdo em Formato de Aula',
    'Guia do Atendimento Magnético',
]

def api_get(page, url, account_id=None):
    headers = "{'Content-Type': 'application/json'" + (f", 'x-zouti-account': '{account_id}'" if account_id else "") + "}"
    return page.evaluate(f"""async () => {{
        const r = await fetch('{url}', {{
            credentials: 'include',
            headers: {headers}
        }});
        return await r.json();
    }}""")

def get_orders(page, account_id, date_str, status='PAID'):
    url = (f'https://apiv1.zouti.com.br/v1/accounts/{account_id}/orders'
           f'?page=1&limit=100&start_date={date_str}&end_date={date_str}&status={status}')
    return api_get(page, url, account_id)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context().new_page()

    print("Fazendo login...")
    page.goto('https://dashboard.zouti.com.br/login')
    page.wait_for_load_state('networkidle')
    page.click('text=Sou Produtor')
    time.sleep(1)
    page.fill('#email', EMAIL)
    page.fill('#password', PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_selector('button:has-text("Vendas")', timeout=15000)
    print("Logado!\n")

    for account_name, account_id in ACCOUNTS.items():
        print(f"=== {account_name} — pedidos de {DATE} ===")

        # Navegar para a conta
        page.goto(f'https://dashboard.zouti.com.br/{account_id}/dashboard/infoproduct/sales/orders')
        time.sleep(3)

        data = get_orders(page, account_id, DATE)
        print(f"Estrutura da resposta: {list(data.keys()) if isinstance(data, dict) else type(data)}")

        if isinstance(data, dict) and 'object' in data:
            orders = data['object']
            print(f"Total de pedidos: {len(orders)}")
            orders_list = list(orders.values()) if isinstance(orders, dict) else orders
            if orders_list:
                # Mostrar primeiro pedido pra entender a estrutura
                print("\nPrimeiro pedido (estrutura):")
                first = orders_list[0]
                print(f"  Keys: {list(first.keys())}")
                print(f"  status: {first.get('status')}")
                print(f"  total: {first.get('total')}")
                # Tentar achar o produto
                for key in ['product', 'products', 'line_items', 'items', 'infoproduct']:
                    if key in first:
                        print(f"  {key}: {json.dumps(first[key], ensure_ascii=False)[:200]}")
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
        print()

    browser.close()
