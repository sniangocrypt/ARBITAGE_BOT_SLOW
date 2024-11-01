import requests
from collections import OrderedDict
from colorama import Fore, Back, Style
import json
import time

tokens = ["BTC", "ETH", "SOL", "XLM", "DOGE", "TON", "MOVR", "GLMR", "MINA", "TWT"]


def parse_kucoin():
	kucoin_dict = {}
	kucoin_url = f"https://api.kucoin.com/api/v1/market/allTickers"
	kucoin_response = requests.get(url=kucoin_url)
	data = kucoin_response.json()
	kucoin_response.close()
	for ticker in data['data']['ticker']:
		if ticker['symbol'][:-5] in tokens and ticker['symbol'][-5:] == "-USDT":
			kucoin_dict[ticker['symbol']] = ticker['last']
	with open("Kucoin.json", "w", encoding="utf-8") as file:
		json.dump(kucoin_dict, file, ensure_ascii=True, indent=4)
	return kucoin_dict


def parse_binance():
	binance_dict = {}
	binance_url = "https://api.binance.com/api/v3/ticker/price"
	binance_response = requests.get(url=binance_url)
	data = binance_response.json()
	binance_response.close()
	for ticker in data:
		for token in tokens:
			if ticker['symbol'] == f"{token}USDT":
				binance_dict[ticker['symbol']] = ticker['price']
				break
	with open("Binance.json", "w", encoding="utf-8") as file:
		json.dump(binance_dict, file, ensure_ascii=True, indent=4)
	return binance_dict


def calculate_spread(binance_data: dict, kucoin_data: dict):
	if (not binance_data) or (not kucoin_data):
		print("Не удалось получить цены по токенам с одной из бирж! Расчет спреда невозможен!")
		return None
	sorted_binance_data = OrderedDict(sorted(binance_data.items()))
	sorted_kucoin_data = OrderedDict(sorted(kucoin_data.items()))
	for binance_token, kucoin_token in zip(sorted_binance_data, sorted_kucoin_data):
		if binance_token == kucoin_token.replace("-", ""):
			print(Fore.RED + f"Рассматриваем тикер: {binance_token}")
			if float(sorted_binance_data[binance_token]) / float(sorted_kucoin_data[kucoin_token]) >= 1.001:
				print("Направление Kucoin -> Binance")
				print(f"Профит в %: {(float(sorted_binance_data[binance_token]) / float(sorted_kucoin_data[kucoin_token]) - 1) * 100}%")
				print(f"Профит в $: {float(sorted_binance_data[binance_token]) - float(sorted_kucoin_data[kucoin_token])}$")
			elif float(sorted_kucoin_data[kucoin_token]) / float(sorted_binance_data[binance_token]) >= 1.001:
				print("Направление Binance -> Kucoin")
				print(f"Профит в %: {(float(sorted_kucoin_data[kucoin_token]) / float(sorted_binance_data[binance_token]) - 1) * 100}%")
				print(f"Профит в $: {float(sorted_kucoin_data[kucoin_token]) - float(sorted_binance_data[binance_token])}$")
			else:
				print(Fore.RED + f"Арбтиража нет БЛЯТЬ, ищем дальше...")
			print("="*20)


def main():
	calculate_spread(parse_binance(), parse_kucoin())
start_time = time.time()
main()
end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения функции: {execution_time} секунд")
