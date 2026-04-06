"""
auth_sheets.py — Autentica com Google Sheets e salva o token em disco.
Rodar uma vez: python3 auth_sheets.py
Depois o zouti_sheets.py usa o token salvo automaticamente.
"""
import os, sys, json
sys.path.insert(0, '/Users/matheusjorel/Library/Python/3.9/lib/python/site-packages')

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')
CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Renovando token...")
            creds.refresh(Request())
        else:
            print("Iniciando autenticação OAuth...")
            client_config = {
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uris": ["http://localhost"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print(f"Token salvo em {TOKEN_FILE}")

    return creds

if __name__ == '__main__':
    creds = get_credentials()
    print(f"Autenticado! Token válido: {creds.valid}")
    print(f"Expira em: {creds.expiry}")
