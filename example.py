import asyncio

from mercapi import Mercapi


async def main():
    mercapi = Mercapi()
    results = await mercapi.search('sharpnel')
    print(results.as_dict())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
