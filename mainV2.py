import requests
import asyncio
from aiohttp import ClientSession
from collections import OrderedDict
import time
import random
import json
import aiofiles

dict = []

range = 1.001


async def get_okx_info():
    async with ClientSession() as session:
        url = f'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
        headers = {
            'Accept': 'application/json',
        }
        async with session.get(url=url, headers=headers) as response:
            data = await response.json()
        okx = []
        for ticker in data['data']:
            if ticker['instId'][-5:] == "-USDT":
                dict.append(ticker['instId'][:-5])
                okx.append(ticker)
#        print(dict)
        async with aiofiles.open('okxbook.json', 'w') as file:
            await file.write(json.dumps(okx, indent=4))



async def get_binance_info():
    await get_okx_info()
    async with ClientSession() as session:
        url = f'https://api.binance.com/api/v3/ticker/price'
        headers = {
            'Accept': 'application/json',
        }
        async with session.get(url=url, headers=headers) as response:
            data = await response.json()
            binance = []
            for ticker in data:
                if ticker['symbol'][-4:] == "USDT" and ticker['symbol'][:-4] in dict:
                    binance.append(ticker)
#                    print(ticker)
        async with aiofiles.open('binancebook.json', 'w') as file:
            await file.write(json.dumps(binance, indent=4))



async def get_bybit_info():
    await get_okx_info()
    async with ClientSession() as session:
        url = f'https://api.bybit.com/v5/market/tickers?category=spot'
        headers = {
            'Accept': 'application/json',
        }
        async with session.get(url=url, headers=headers) as response:
            data = await response.json()
            bybit = []
            for ticker in data['result']['list']:
                if ticker['symbol'][-4:] == "USDT" and ticker['symbol'][:-4] in dict:
                    bybit.append(ticker)
#                    print(bybit)
        async with aiofiles.open('bybitbook.json', 'w') as file:
            await file.write(json.dumps(bybit, indent=4))


async def checker():
    await get_okx_info()
    await get_bybit_info()
    await get_binance_info()
    async with aiofiles.open('binancebook.json', 'r') as file:
        data_binance = await file.read()
    async with aiofiles.open('bybitbook.json', 'r') as file:
        data_bybit = await file.read()
    async with aiofiles.open('okxbook.json', 'r') as file:
        data_okx = await file.read()
    binance_check = json.loads(data_binance)
    bybit_check = json.loads(data_bybit)
    okx_check = json.loads(data_okx.replace("-", ""))
    for binance, bybit, okx in zip(binance_check, bybit_check, okx_check):\

# ЧЕКАЕМ РАЗНИЦУ БИНАНСА И БУБИТА В 2 СТОРОНЫ (Б/БУ) (БУ/Б)

        if binance['symbol'] == bybit['symbol']:
            if float(binance['price']) / float(bybit['lastPrice']) >= range:
                print("Arbitrage detected")
                print(binance['symbol'])
                print("Направление BINANCE - BYBIT")
                print(f"Разница в цене {(((float(binance['price'])/float(bybit['lastPrice'])) - 1) * 100)}%")
            elif float(bybit['lastPrice'])/float(binance['price']) >= 1.01:
                print("Arbitrage detected")
                print(bybit['symbol'])
                print("Направление BYBIT - BINANCE")
                print(f"Разница в цене {(((float(bybit['lastPrice'])/float(binance['price'])) - 1) * 100)}%")

# ЧЕКАЕМ РАЗНИЦУ БИНАНСА И ОКХ В 2 СТОРОНЫ (Б/О) (О/Б)

        elif binance['symbol'] == okx['instId']:
            if float(binance['price']) / float(okx['last']) >= range:
                print("Arbitrage detected")
                print(binance['symbol'])
                print("Направление BINANCE - OKX")
                print(f"Разница в цене {(((float(binance['price'])/float(okx['last'])) - 1) * 100)}%")
            elif float(okx['last']) / float(binance['symbol']) >= range:
                print("Arbitrage detected")
                print(okx['instId'])
                print("Направление OKX - BINANCE")
                print(f"Разница в цене {(((float(okx['last']) / float(binance['symbol'])) - 1) * 100)}%")

# ЧЕКАЕМ РАЗНИЦУ БУБИТ И ОКХ В 2 СТОРОНЫ (БУ/О) (О/БУ)
        elif bybit['symbol'] == okx['instId']:
            if float(bybit['lastPrice']) / float(okx['last']) >= range:
                print("Arbitrage detected")
                print(bybit['symbol'])
                print("Направление BYBIT - OKX")
                print(f"Разница в цене {(((float(bybit['lastPrice'])/float(okx['last'])) - 1) * 100)}%")
            elif float(okx['last']) / float(bybit['lastPrice']) >= range:
                print("Arbitrage detected")
                print(okx['instId'])
                print("Направление OKX - BYBIT")
                print(f"Разница в цене {(((float(okx['last']) / float(bybit['lastPrice'])) - 1) * 100)}%")

        else:print("НИЧЕГО НЕ НАШЛИ")
            






async def main():
#    tasks = [checker()]
#    await asyncio.gather(*tasks)
    await checker()


print("Start Time:", time.strftime('%X'))
asyncio.run(main())
print("End Time:", time.strftime('%X'))
