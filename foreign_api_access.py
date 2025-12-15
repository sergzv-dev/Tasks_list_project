import requests
import asyncio
import httpx
from itertools import count

url = 'http://37.60.242.21:58000/users'
timeout = httpx.Timeout(10.0)

async def fetch(client, url, *, page: int, size: int):
    params = {'page': page, 'size': size}
    for _ in range(3):
        r = await client.get(url, params = params)
        status = r.status_code
        if status == 200: return r.json()


async def main():
    async with httpx.AsyncClient(timeout=timeout) as client:
        pool = 50

        for start in count(start=1, step=pool):

            tasks = [fetch(client, url, page=page, size=20) for page in range(start, start + pool)]

            result = await asyncio.gather(*tasks)
            print(result)
            for res in result:
                print(res)

                users = res['items']

                if len(users) == 0: return None

                for user in users:
                    if user['name'] == 'Sarah Connor': return user['user_id']

result = asyncio.run(main())
print(result)


