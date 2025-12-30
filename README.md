# 仮想通貨価格取得スクリプト
このリポジトリの `get_price.py` は、CoinGecko APIを利用して以下の仮想通貨（ETH, USDT, USDC, BTC, hyperliquid, MIYAKO）の過去1年間の日次価格（USD/JPY）を取得し、CSVファイルとして出力するPythonスクリプト

## 取得対象通貨
- ETH（Ethereum）
- USDT（Tether）
- USDC（USD Coin）
- BTC（Bitcoin）
- hyperliquid
- MIYAKO
- SOL（Solana）
- LINEA


  



## 出力ファイル
- `crypto_prices.csv`
  - 各日付ごとに全通貨のUSD価格・JPY価格が記録されます。
		- ヘッダー例：
			```
			date,ETH_USD,USDT_USD,USDC_USD,BTC_USD,hyperliquid_USD,MIYAKO_USD,SOL_USD,LINEA_USD,ETH_JPY,USDT_JPY,USDC_JPY,BTC_JPY,hyperliquid_JPY,MIYAKO_JPY,SOL_JPY,LINEA_JPY
			```

## 使い方
1. 必要なPythonパッケージをインストールしてください。
	```bash
	pip install requests
	```
2. `get_price.py` を実行します。
	```bash
	python get_price.py
	```
3. 実行後、同じディレクトリに `crypto_prices.csv` が生成されます。

## 注意事項
- CoinGecko APIの仕様上、リクエスト間隔を空けています（API制限対策）。
- hyperliquidやMIYAKOのCoinGecko IDが変更された場合は、スクリプト内のIDを修正してください。
- 取得期間や通貨はスクリプト内で変更可能です。
- 動作は未確認
---

