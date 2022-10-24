# mercapi

![PyPI](https://img.shields.io/pypi/v/mercapi)
[![Tests](https://github.com/take-kun/mercapi/actions/workflows/check.yaml/badge.svg?branch=main)](https://github.com/take-kun/mercapi/actions/workflows/check.yaml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mercapi)

[API Documentation](https://take-kun.github.io/mercapi/)

## What is Mercapi?

Mercapi is a Python wrapper for *mercari.jp* API.
It's capable of producing HTTP requests implementing security mechanisms employed in native *mercari.jp* web app.
Requests and responses are mapped to custom classes with type-hinting and documentation.

## Quickstart

First, install the `mercapi` package using the package manager of your choice.

As an example, we want to run the search query `sharpnel`.

```python
from mercapi import Mercapi


m = Mercapi()
results = await m.search('sharpnel')

print(f'Found {results.meta.num_found} results')
for item in results.items:
    print(f'Name: {item.name}\\nPrice: {item.price}\\n')

```

We can use a single result object to retrieve full details of the listing.
```python
item = results.items[0]
full_item = await item.full_item()

print(full_item.description)
```

Or get it directly using an ID.
```python
item = await m.item('m90925725213')

print(item.description)
```

Refer to `mercapi.mercapi.Mercapi` documentation for all implemented features.

*Examples above are not executable. If you want to try them out, run `python example.py`.*