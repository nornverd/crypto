import requests
import datetime
import time

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

# 結果表示例
for row in results[:5]:
    print(row)