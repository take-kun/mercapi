import asyncio
import logging

from mercapi import Mercapi


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


async def main():
    m = Mercapi()
    results = await m.search('sharpnel')

    print(f'Found {results.meta.num_found} results')
    for item in results.items:
        print(f'Name: {item.name}\nPrice: {item.price}\n')

    item = results.items[0]
    full_item = await item.full_item()
    print(full_item.description)

    item = await m.item('m64017471338')
    print(item.description)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
