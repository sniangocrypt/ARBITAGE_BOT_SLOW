import requests
import requests
from colorama import Fore, Back, Style
import json

# tokens from excchenge

tokens = ["BTC","ETH","SOL","XLM","DOGE"]
tokenss = tokens[0]

# ПОЛУЧЕМ ЦЕНУ С КУКОИНА

SYMBOL = f"{tokenss}-USDT"

url = f"https://api.kucoin.com/api/v1/market/allTickers"
response = requests.get(url)
r = response.json()

for token in r["data"]["ticker"]:
	symbol = token["symbol"]
	price = token["last"]
	if symbol == SYMBOL:
		print(Fore.GREEN +f"Цена {tokenss}  нa куоине {price}")
		price_kukoin = float(price)
	with open("venv\kukoin.json", "w", encoding="utf-8") as file:
		json.dump(price, file, ensure_ascii=False, indent=4)

# ПОЛУЧЕМ ЦЕНУ С БИНАНСА

SYMBOL_BINANCE = {
  "symbol": f"{tokenss}USDT",
}
#f""symbol"': "{tokens[1]}USDT""
url = "https://api.binance.com/api/v3/ticker/price"
params = SYMBOL_BINANCE
response_binance = requests.get(url= url, params = params)
BINANCE = response_binance.json()
price_binane = float(BINANCE['price'])
print(f"Цена {tokenss} на биненсе {BINANCE['price']}")
with open("venv\BINANCE.json", "w", encoding="utf-8") as file:
	json.dump(price, file, ensure_ascii=False, indent=4)



if (price_kukoin/price_binane) >= 1.05:
	print(f"Разница в цене {tokenss} KUKOIN/BINANCE = {(((price_kukoin/price_binane)-1)*100)}%")
elif (price_binane/price_kukoin) >= 1.05:
	print(f"Разница в цене {tokenss} BINANCE/KUKOIN = {(((price_binane/price_kukoin)-1)*100)} %")
else:
	print(Fore.RED +f"Арбтиража нет БЛЯТЬ, ищем дальше...")
	print()

for i in range(4):
	tokenss = tokens[i+1]
	print(Fore.GREEN + f"Цена {tokenss}  нa куоине {price}")
	print(f"Цена {tokenss} на биненсе {BINANCE['price']}")
	if (price_kukoin / price_binane) >= 1.05:
		print(f"Разница в цене {tokenss} KUKOIN/BINANCE = {(((price_kukoin / price_binane) - 1) * 100)}%")
	elif (price_binane / price_kukoin) >= 1.05:
		print(f"Разница в цене {tokenss} BINANCE/KUKOIN = {(((price_binane / price_kukoin) - 1) * 100)} %")
	else:
		print(Fore.RED +f"Арбтиража нет БЛЯТЬ, ищем дальше...")
		print()
		error = 1

if error == 1:
	print()
	print(Fore.RED +"ПИЗДЕЦ, ВЕЗДЕ ПУСТО...")
