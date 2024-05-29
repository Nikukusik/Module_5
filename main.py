import aiohttp
import asyncio
import sys
import datetime as dt
from datetime import datetime as dtdt


async def main(days: int):
    res = []
    async with aiohttp.ClientSession() as client:
        for day in range(days):
            res.append(await worker(client, day))

    return res

async def worker(client: aiohttp.ClientSession, day: int):
    today_date = dtdt.now().date()
    needed_date = (today_date - dt.timedelta(day)).strftime('%d.%m.%Y')
    try:
        async with client.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={needed_date}') as response:
            if response.ok:
                data = await response.json()
                currents = data.get("exchangeRate")
                new_data = {needed_date: {}}
                for current in currents:
                    if current["currency"] == "USD":
                        new_data[needed_date]["USD"] = {'sale': current.get('saleRate'), 'purchase': current.get('purchaseRate')}
                    if current["currency"] == "EUR":
                        new_data[needed_date]["EUR"] = {'sale': current.get('saleRate'), 'purchase': current.get('purchaseRate')}
    except aiohttp.ClientError as err:
        print(f"Error getting data for date {needed_date}: {err}")
                        

    return new_data




if __name__ == "__main__":
    if int(sys.argv[1]) <= 10:
        res = asyncio.run(main(days = int(sys.argv[1])))
    print(res)
