"""
zouti_sheets.py — Busca vendas e faturamento da Zouti e atualiza Google Sheets (MAT09)

Uso:
  python3 zouti_sheets.py                        → roda para ontem
  python3 zouti_sheets.py --date 2026-05-22      → data específica
  python3 zouti_sheets.py --dry-run              → mostra os dados sem gravar
  python3 zouti_sheets.py --explore              → mostra estrutura de um pedido (pra debugar campos)
"""

import os, sys, time, json, argparse, urllib.parse, urllib.request, urllib.error
from datetime import date, timedelta, datetime
from collections import defaultdict

sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# ── Configuração ──────────────────────────────────────────────────────────────

ZOUTI_EMAIL    = os.getenv('ZOUTI_EMAIL')
ZOUTI_PASSWORD = os.getenv('ZOUTI_PASSWORD')
SPREADSHEET_ID = os.getenv('SPREADSHEET_LBR')
ACCOUNT_ID     = 'acc_xhhpimoyb18g139fen6brn'
SHEET_TAB      = 'MAT | 09- Junho'
TOKEN_FILE     = os.path.join(os.path.dirname(__file__), 'token.json')

# Nomes exatos dos produtos na Zouti (confirmar com --explore se mudar de edição)
PRODUCTS = {
    'main': 'Imersão Mestres da Audiência Trabalhista | 9ª Edição',
    'ob1':  'Imersão Mestres da Audiência Trabalhista | 9ª Edição - Conteúdo em Formato de Aulas',
    'ob2':  'Ônus da Prova',
}

# Linhas na planilha (1-based)
ROWS = {
    'venda_main': 26,
    'venda_ob1':  36,
    'venda_ob2':  37,
    'fat_main':   41,
    'fat_ob1':    42,
    'fat_ob2':    43,
}

# ── Zouti: login e pedidos ─────────────────────────────────────────────────────

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

def navigate_to_account(page):
    page.goto(f'https://dashboard.zouti.com.br/{ACCOUNT_ID}/dashboard/infoproduct/sales/orders')
    time.sleep(2)

def fetch_orders(page, date_str):
    """Busca todos os pedidos PAID de uma data com paginação."""
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
            print(f"  Erro na API Zouti: {data}")
            break

        meta   = data['object']
        orders = meta.get('data', [])
        all_orders.extend(orders)

        total_pages = meta.get('total_pages', 1)
        if current_page >= total_pages:
            break
        current_page += 1

    return all_orders

def aggregate(orders):
    """Retorna contagem e faturamento líquido por produto."""
    vendas = defaultdict(int)
    fat    = defaultdict(float)

    for order in orders:
        for product in order.get('products', []):
            name = product.get('name', '').strip()
            for key, expected in PRODUCTS.items():
                if name.lower() == expected.lower():
                    vendas[key] += 1
                    # Faturamento líquido: preferir net_amount, fallback para amount ou total
                    net = (
                        product.get('net_amount')
                        or product.get('net_value')
                        or product.get('amount_net')
                    )
                    if net is None:
                        # Tenta no nível do pedido se não tiver no produto
                        net = order.get('net_amount') or order.get('net_value') or 0
                    fat[key] += float(net or 0)

    return vendas, fat

# ── Google Sheets ─────────────────────────────────────────────────────────────

def load_token():
    """Carrega token OAuth do token.json gerado pelo auth_sheets.py."""
    if not os.path.exists(TOKEN_FILE):
        print(f"Token não encontrado em {TOKEN_FILE}.")
        print("Rode primeiro: python3 auth_sheets.py")
        return None

    sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds.token

def find_date_column(grid, target_date):
    """Encontra o índice (0-based) da coluna com a data alvo."""
    target = datetime.strptime(target_date, '%Y-%m-%d')

    for row in grid:
        for i, cell in enumerate(row):
            cell_str = str(cell).strip()
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

def col_letter(col_index):
    """Converte índice 0-based para letra de coluna (A, B, ..., AA, AB, ...)."""
    letter = ''
    n = col_index + 1
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letter = chr(65 + rem) + letter
    return letter

def read_range(access_token, range_notation):
    url = (f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/'
           f'{urllib.parse.quote(range_notation)}')
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {access_token}')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()).get('values', [])

def write_cell(access_token, range_notation, value):
    url = (f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/'
           f'{urllib.parse.quote(range_notation)}?valueInputOption=USER_ENTERED')
    body = json.dumps({'values': [[value]]}).encode()
    req = urllib.request.Request(url, data=body, method='PUT')
    req.add_header('Authorization', f'Bearer {access_token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {'error': e.read().decode()}

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date',    help='Data no formato YYYY-MM-DD (padrão: ontem)')
    parser.add_argument('--dry-run', action='store_true', help='Mostra os dados sem gravar na planilha')
    parser.add_argument('--explore', action='store_true', help='Mostra a estrutura de um pedido (debug)')
    args = parser.parse_args()

    target_date = args.date or (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"Data: {target_date}")
    if args.dry_run:  print("Modo: dry-run (sem gravar)")
    if args.explore:  print("Modo: explore (mostra estrutura dos pedidos)")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_context().new_page()

        print("Fazendo login na Zouti...")
        login(page)
        navigate_to_account(page)
        print("Logado.\n")

        print(f"Buscando pedidos PAID de {target_date}...")
        orders = fetch_orders(page, target_date)
        print(f"{len(orders)} pedido(s) encontrado(s)\n")

        if args.explore:
            if orders:
                print("── Estrutura do primeiro pedido ──")
                print(json.dumps(orders[0], indent=2, ensure_ascii=False))
                print("\n── Todos os produtos encontrados ──")
                seen = set()
                for o in orders:
                    for prod in o.get('products', []):
                        name = prod.get('name', '').strip()
                        if name not in seen:
                            seen.add(name)
                            fields = {k: prod.get(k) for k in ['name','price','amount','net_amount','net_value','amount_net','total']}
                            print(json.dumps(fields, ensure_ascii=False))
            else:
                print("Nenhum pedido encontrado para explorar.")
            browser.close()
            return

        vendas, fat = aggregate(orders)
        browser.close()

    print("── Resultado ──")
    for key in ['main', 'ob1', 'ob2']:
        print(f"  {key}: {vendas[key]} vendas | R$ {fat[key]:.2f} faturamento líquido")
    print()

    if args.dry_run:
        print("[dry-run] Nada gravado.")
        return

    # Autenticação Sheets
    access_token = load_token()
    if not access_token:
        return

    # Descobrir coluna da data
    header_range = f"'{SHEET_TAB}'!A1:AQ8"
    grid = read_range(access_token, header_range)
    col_idx = find_date_column(grid, target_date)
    if col_idx is None:
        print(f"Data {target_date} não encontrada na planilha. Verifique se está dentro do intervalo do MAT09.")
        return

    col = col_letter(col_idx)
    print(f"Coluna da data {target_date}: {col} (índice {col_idx})\n")

    # Escrever células
    cells = [
        (ROWS['venda_main'], vendas['main'],  'Venda Principal'),
        (ROWS['venda_ob1'],  vendas['ob1'],   'Venda OB1'),
        (ROWS['venda_ob2'],  vendas['ob2'],   'Venda OB2'),
        (ROWS['fat_main'],   fat['main'],     'Fat. Principal'),
        (ROWS['fat_ob1'],    fat['ob1'],      'Fat. OB1'),
        (ROWS['fat_ob2'],    fat['ob2'],      'Fat. OB2'),
    ]

    print("── Gravando na planilha ──")
    for row, value, label in cells:
        cell_range = f"'{SHEET_TAB}'!{col}{row}"
        result = write_cell(access_token, cell_range, value)
        status = 'OK' if 'updatedCells' in result else f"ERRO: {result}"
        print(f"  {label} ({cell_range}): {value} → {status}")

    print("\nConcluído!")

if __name__ == '__main__':
    main()
