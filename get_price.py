import requests
import datetime
import time
import csv

coins = ['ETH', 'USDT', 'USDC', 'BTC']
base_currency = 'USD'
fiat_currency = 'JPY'

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

def get_coinbase_price(coin, currency, date):
    iso_date = date.isoformat()
    url = f'https://api.coinbase.com/v2/prices/{coin}-{currency}/spot?date={iso_date}'
    r = requests.get(url)
    try:
        return float(r.json()['data']['amount'])
    except Exception:
        return None

results = []
for single_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
    usd_jpy = get_coinbase_price('USD', fiat_currency, single_date)
    for coin in coins:
        usd_price = get_coinbase_price(coin, base_currency, single_date)
        if usd_price and usd_jpy:
            jpy_price = usd_price * usd_jpy
            results.append({
                'date': single_date.strftime('%Y-%m-%d'),
                'coin': coin,
                'usd': usd_price,
                'jpy': jpy_price
            })
    time.sleep(0.2)  # API制限対策


# CSV出力処理
csv_filename = 'crypto_prices.csv'
header = ['date'] + [f'{coin}_USD' for coin in coins] + [f'{coin}_JPY' for coin in coins]

# 日付ごとに各通貨の価格をまとめる
date_dict = {}
for row in results:
    d = row['date']
    coin = row['coin']
    if d not in date_dict:
        date_dict[d] = {}
    date_dict[d][f'{coin}_USD'] = row['usd']
    date_dict[d][f'{coin}_JPY'] = row['jpy']

with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for d in sorted(date_dict.keys()):
        row = [d]
        for coin in coins:
            row.append(date_dict[d].get(f'{coin}_USD', ''))
        for coin in coins:
            row.append(date_dict[d].get(f'{coin}_JPY', ''))
        writer.writerow(row)

print(f'CSVファイル {csv_filename} に出力しました')