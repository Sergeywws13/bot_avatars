import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import CREDS_FILE, SHEET_NAME

scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scopes)
client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1


def add_booking(service_name: str, username: str, phone: str):
    """Записать новую заявку в Google Sheets"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([now, service_name, username, phone])


def get_all_bookings():
    """Получить все записи из таблицы"""
    return sheet.get_all_records()
