import asyncio
import logging

from mercapi import Mercapi


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


async def main():
    mercapi = Mercapi()
    results = await mercapi.search('sharpnel')
    print(results.items[0].name, results.items[0].price)
    item = await mercapi.item('m94786104879')
    print(item.name, item.price, item.status)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
