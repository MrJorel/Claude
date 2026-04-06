"""
zouti_sheets.py — Busca vendas aprovadas de ontem na Zouti e atualiza Google Sheets

Fluxo:
1. Login no Zouti via Playwright
2. Para cada conta (LBR e Wizoom), busca pedidos PAID do dia anterior via API
3. Conta vendas por produto (principal + orderbumps)
4. Escreve na coluna do dia correto na planilha

Execução: python3 zouti_sheets.py
           python3 zouti_sheets.py --date 2026-04-04  (forçar data específica)
"""

import os, sys, time, json, argparse
from datetime import date, timedelta
from collections import defaultdict

sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# ── Configuração ──────────────────────────────────────────────────────────────

ZOUTI_EMAIL    = os.getenv('ZOUTI_EMAIL')
ZOUTI_PASSWORD = os.getenv('ZOUTI_PASSWORD')

ACCOUNTS = {
    'lbr':    'acc_xhhpimoyb18g139fen6brn',
    'wizoom': 'acc_1idr3k8zzv9480cah4d50z',
}

SPREADSHEETS = {
    'lbr':    os.getenv('SPREADSHEET_LBR'),
    'wizoom': os.getenv('SPREADSHEET_WIZOOM'),
}

SHEET_TABS = {
    'lbr':    'MAT | 08- Abril',
    'wizoom': 'IEA | 02 - Abril',
}

SHEET_IDS = {
    'lbr':    1799837654,
    'wizoom': 10554169,
}

# Produtos do funil (nome exato como aparece na Zouti)
PRODUCTS = {
    'lbr': {
        'main':  'Imersão Mestres da Audiência Trabalhista | 8º Edição',
        'ob1':   'Imersão Mestres da Audiência Trabalhista | 8º Edição - Conteúdo em Formato de Aulas',
        'ob2':   'Ônus da Prova',
    },
    'wizoom': {
        'main': 'Imersão Estética Automotiva 30K | 2ª Edição',
        'ob1':  'Imersão Estética Automotiva 30K | 2º Edição - Conteúdo em Formato de Aula',
        'ob2':  'Guia do Atendimento Magnético',
    },
}

# Linhas na planilha (1-based) para cada produto
SHEET_ROWS = {
    'lbr': {
        'main': 26,  # # Venda Real Produto Principal
        'ob1':  36,  # # Venda Real ORDERBUMP #1
        'ob2':  37,  # # Venda Real ORDERBUMP #2
    },
    'wizoom': {
        'main': 26,
        'ob1':  36,
        'ob2':  37,
    },
}

# ── Zouti API ─────────────────────────────────────────────────────────────────

def login(page):
    page.goto('https://dashboard.zouti.com.br/login')
    page.wait_for_load_state('networkidle')
    page.click('text=Sou Produtor')
    time.sleep(1)
    page.fill('#email', ZOUTI_EMAIL)
    page.fill('#password', ZOUTI_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_selector('button:has-text("Vendas")', timeout=20000)
    time.sleep(1)

def get_orders(page, account_id, date_str):
    """Busca todos os pedidos PAID de uma data (com paginação)."""
    all_orders = []
    current_page = 1

    while True:
        url = (f'https://apiv1.zouti.com.br/v1/accounts/{account_id}/orders'
               f'?page={current_page}&per_page=100&start_date={date_str}&end_date={date_str}&status=PAID')

        data = page.evaluate(f"""async () => {{
            const r = await fetch('{url}', {{
                credentials: 'include',
                headers: {{
                    'Content-Type': 'application/json',
                    'x-zouti-account': '{account_id}'
                }}
            }});
            return await r.json();
        }}""")

        if 'object' not in data:
            print(f"  Erro na API: {data}")
            break

        meta = data['object']
        orders = meta.get('data', [])
        all_orders.extend(orders)

        total_pages = meta.get('total_pages', 1)
        if current_page >= total_pages:
            break
        current_page += 1

    return all_orders

def count_products(orders, product_map):
    """Conta vendas por tipo de produto."""
    counts = defaultdict(int)
    for order in orders:
        for product in order.get('products', []):
            name = product.get('name', '').strip()
            for key, expected_name in product_map.items():
                if name.lower() == expected_name.lower().strip():
                    counts[key] += 1
    return counts

# ── Google Sheets ─────────────────────────────────────────────────────────────

def get_sheets_service():
    """Retorna cliente autenticado do Google Sheets."""
    # Usar o google-auth com Application Default Credentials ou token OAuth salvo
    # Por enquanto usa o token do MCP server que já está configurado
    import subprocess, json as _json

    # Tenta pegar o token do servidor MCP em execução
    try:
        result = subprocess.run(
            ['node', '-e', '''
                const fs = require('fs');
                const paths = [
                    process.env.HOME + '/.config/google-sheets-mcp/tokens.json',
                    process.env.HOME + '/.google-sheets-mcp/tokens.json',
                    '/tmp/google-sheets-tokens.json'
                ];
                for (const p of paths) {
                    if (fs.existsSync(p)) {
                        const t = JSON.parse(fs.readFileSync(p));
                        console.log(JSON.stringify(t));
                        process.exit(0);
                    }
                }
                console.log("{}");
            '''],
            capture_output=True, text=True, timeout=5
        )
        tokens = _json.loads(result.stdout.strip() or '{}')
        if tokens.get('access_token'):
            return tokens['access_token']
    except:
        pass
    return None

def find_date_column(page_data, target_date):
    """Encontra a coluna (índice 0-based) correspondente a uma data nas linhas de header."""
    # target_date no formato 'YYYY-MM-DD'
    from datetime import datetime
    target = datetime.strptime(target_date, '%Y-%m-%d')

    for row in page_data:
        for i, cell in enumerate(row):
            cell_str = str(cell).strip()
            # Tenta parsear como data no formato DD/MM ou DD/MM/YYYY
            for fmt in ['%d/%m/%Y', '%d/%m', '%d-%m-%Y', '%d-%m']:
                try:
                    parsed = datetime.strptime(cell_str, fmt)
                    if fmt in ['%d/%m', '%d-%m']:
                        parsed = parsed.replace(year=target.year)
                    if parsed.month == target.month and parsed.day == target.day:
                        return i
                except:
                    pass
    return None

def update_sheet(access_token, spreadsheet_id, sheet_tab, row, col_index, value):
    """Atualiza uma célula na planilha."""
    import urllib.request, urllib.error

    # Converte índice de coluna para letra A1
    col_letter = ''
    n = col_index + 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        col_letter = chr(65 + remainder) + col_letter

    range_notation = f"'{sheet_tab}'!{col_letter}{row}"
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{urllib.parse.quote(range_notation)}?valueInputOption=USER_ENTERED"

    body = json.dumps({'values': [[value]]}).encode()
    req = urllib.request.Request(url, data=body, method='PUT')
    req.add_header('Authorization', f'Bearer {access_token}')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {'error': e.read().decode()}

# ── Busca token OAuth ─────────────────────────────────────────────────────────

def find_oauth_token():
    """Procura token OAuth salvo pelo MCP server do Google Sheets."""
    import glob
    paths = glob.glob(os.path.expanduser('~/.config/**/tokens*.json'), recursive=True)
    paths += glob.glob(os.path.expanduser('~/.google*/**/*.json'), recursive=True)
    paths += glob.glob('/tmp/google*.json')

    for p in paths:
        try:
            with open(p) as f:
                data = json.load(f)
            if isinstance(data, dict) and data.get('access_token'):
                print(f"  Token encontrado em: {p}")
                return data['access_token']
        except:
            pass

    return None

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='Data no formato YYYY-MM-DD (padrão: ontem)')
    parser.add_argument('--dry-run', action='store_true', help='Não escreve na planilha')
    args = parser.parse_args()

    target_date = args.date or (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"Data alvo: {target_date}")
    print(f"Dry run: {args.dry_run}\n")

    # Buscar token do Google Sheets
    access_token = find_oauth_token()
    if not access_token and not args.dry_run:
        print("AVISO: Token do Google Sheets não encontrado. Certifique-se que o servidor MCP está rodando.")
        print("Continuando em modo dry-run...")
        args.dry_run = True

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context().new_page()

        print("Fazendo login no Zouti...")
        login(page)
        print("Logado!\n")

        for client, account_id in ACCOUNTS.items():
            print(f"── {client.upper()} ──")

            # Navegar para a conta
            page.goto(f'https://dashboard.zouti.com.br/{account_id}/dashboard/infoproduct/sales/orders')
            time.sleep(2)

            # Buscar pedidos
            print(f"  Buscando pedidos de {target_date}...")
            orders = get_orders(page, account_id, target_date)
            print(f"  {len(orders)} pedidos encontrados")

            # Contar por produto
            counts = count_products(orders, PRODUCTS[client])
            print(f"  Contagens: {dict(counts)}")
            results[client] = counts

        browser.close()

    print("\n── Resumo ──")
    for client, counts in results.items():
        print(f"\n{client.upper()}:")
        for key, count in counts.items():
            print(f"  {key}: {count}")

    if args.dry_run:
        print("\n[Dry run — planilha não atualizada]")
        return

    # Atualizar planilhas
    print("\n── Atualizando planilhas ──")
    import urllib.parse

    for client, counts in results.items():
        if not any(counts.values()):
            print(f"  {client}: sem vendas, pulando")
            continue

        spreadsheet_id = SPREADSHEETS[client]
        sheet_tab      = SHEET_TABS[client]
        rows           = SHEET_ROWS[client]

        # Ler a linha de datas para achar a coluna certa
        range_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{urllib.parse.quote(sheet_tab + '!A1:AQ5')}"
        req = urllib.request.Request(range_url)
        req.add_header('Authorization', f'Bearer {access_token}')
        with urllib.request.urlopen(req) as resp:
            grid = json.loads(resp.read()).get('values', [])

        # Encontrar coluna da data
        col_idx = find_date_column(grid, target_date)
        if col_idx is None:
            print(f"  {client}: data {target_date} não encontrada na planilha!")
            continue

        print(f"  {client}: coluna {col_idx} para {target_date}")

        for key, count in counts.items():
            row = rows.get(key)
            if row and count > 0:
                result = update_sheet(access_token, spreadsheet_id, sheet_tab, row, col_idx, count)
                print(f"  {client} {key} (linha {row}): {count} → {result}")

    print("\nConcluído!")

if __name__ == '__main__':
    import urllib.parse, urllib.request, urllib.error
    main()
