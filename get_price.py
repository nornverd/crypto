
import requests
import datetime
import time
import csv

# CoinGeckoのIDに合わせる
coins = {
    'ETH': 'ethereum',
    'USDT': 'tether',
    'USDC': 'usd-coin',
    'BTC': 'bitcoin',
    'hyperliquid': 'hyperliquid',  # CoinGecko上のIDが異なる場合は修正してください
    'MIYAKO': 'miyako'
}
base_currency = 'usd'
fiat_currency = 'jpy'

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

def get_coingecko_price(coin_id, date):
    # date: datetime.date型
    date_str = date.strftime('%d-%m-%Y')
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date_str}'
    r = requests.get(url)
    if r.status_code != 200:
        return None, None
    data = r.json()
    try:
        usd = data['market_data']['current_price'][base_currency]
        jpy = data['market_data']['current_price'][fiat_currency]
        return usd, jpy
    except Exception:
        return None, None

results = []
for single_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
    for symbol, coin_id in coins.items():
        usd_price, jpy_price = get_coingecko_price(coin_id, single_date)
        if usd_price is not None and jpy_price is not None:
            results.append({
                'date': single_date.strftime('%Y-%m-%d'),
                'coin': symbol,
                'usd': usd_price,
                'jpy': jpy_price
            })
    time.sleep(1.2)  # CoinGecko API制限対策

# CSV出力処理
csv_filename = 'crypto_prices.csv'
header = ['date'] + [f'{coin}_USD' for coin in coins.keys()] + [f'{coin}_JPY' for coin in coins.keys()]

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
        for coin in coins.keys():
            row.append(date_dict[d].get(f'{coin}_USD', ''))
        for coin in coins.keys():
            row.append(date_dict[d].get(f'{coin}_JPY', ''))
        writer.writerow(row)

print(f'CSVファイル {csv_filename} に出力しました')