from backend.free_search import search
import shelve
import asyncio

SEARCH = {
    'Eric Prince': {
        'strict_terms': 'Eric Prince',
    },
}

class Entry:
    def __init__(self, entry):
        self.title = entry.title
        self.url = entry.url
        self.snippet = entry.snippet
        self.read = False

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url

async def update_all():
    search_entries = [search(**kwargs) for kwargs in SEARCH.values()]
    return await asyncio.gather(*search_entries)

def update_all_blocking():
    results = [set(Entry(e) for e in l) for l in asyncio.run(update_all())]
    with shelve.open('data/store') as db:
        for i, key in enumerate(SEARCH):
            if key not in db:
                db[key] = results[i]
            else:
                db[key] = db[key] | results[i]
