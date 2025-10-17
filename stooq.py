import pandas as pd
import datetime as dt
import os

# === 1️⃣ Ustawienia ===
end_date = dt.date(2025, 10, 17)
start_date = end_date - dt.timedelta(days=365 * 10)  # 10 lat wstecz
folder = "dane"
plik_excel = os.path.join(folder, "dane_stooq.xlsx")

spolki = {
    'TSLA.US': 'Tesla',
    'AAPL.US': 'Apple'
}

# === 2️⃣ Utworzenie folderu, jeśli nie istnieje ===
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"📁 Utworzono folder: {folder}")

# === 3️⃣ Funkcja pobierająca dane ze stooq ===
def pobierz_dane_stooq(ticker):
    url = f"https://stooq.pl/q/d/l/?s={ticker}&d1={start_date.strftime('%Y%m%d')}&d2={end_date.strftime('%Y%m%d')}&i=d"
    df = pd.read_csv(url)
    df['Data'] = pd.to_datetime(df['Date'])
    df = df[['Data', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df

# === 4️⃣ Pobieranie i zapis danych do Excela ===
with pd.ExcelWriter(plik_excel, engine="openpyxl") as writer:
    for ticker, nazwa in spolki.items():
        print(f"⬇️ Pobieram dane: {nazwa} ({ticker})...")
        df = pobierz_dane_stooq(ticker)
        df.to_excel(writer, sheet_name=nazwa, index=False)

print(f"✅ Dane zapisano w pliku: {plik_excel}")
