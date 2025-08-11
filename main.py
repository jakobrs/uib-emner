import asyncio, aiohttp
from bs4 import BeautifulSoup as BS
from types2 import *

URL = "https://www4.uib.no/studier/emner"

rows = []

s = asyncio.Semaphore(15)
async def getpage(session, i):
    global s, rows
    async with s:
        async with session.get(f"{URL}?page={i}") as resp:
            bs = BS(await resp.text())
            for elem in bs.select("a[title][href*=\"/studier\"]"):
                href = elem.get("href")
                title = elem.get("title")
                code = href[href.rindex("/")+1:]
                rows.append(Row(
                    title = title,
                    code = code,
                ))
    print(f"finished {i}", flush=True)


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(getpage(session, i) for i in range(294)))

    print(rows)

asyncio.run(main())
