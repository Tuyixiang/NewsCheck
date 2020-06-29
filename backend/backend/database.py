from backend.free_search import search
import shelve
import asyncio
import datetime

SEARCH = {
    'Erik Prince': {
        'strict_terms': 'Erik Prince',
        'date_range': 3,
    },
}
DB_FILE = 'data/store'
META = "'3\xdd\xa5\xf5oJ\x03"


class Entry:
    def __init__(self, entry):
        if isinstance(entry, str):
            self.url = entry
            self.read = True
        else:
            self.title = entry.title
            self.url = entry.url
            self.snippet = entry.snippet
            self.date = datetime.datetime.now()
            self.read = False

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'date': self.date.isoformat()
        }

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


async def update_all():
    search_entries = [search(**kwargs) for kwargs in SEARCH.values()]
    return await asyncio.gather(*search_entries)


def update_all_blocking(db):
    results = [set(Entry(e) for e in l) for l in asyncio.run(update_all())]
    for i, key in enumerate(SEARCH):
        if key not in db:
            db[key] = results[i]
        else:
            db[key] = db[key] | (results[i] - db[key])


def fetch():
    with shelve.open(DB_FILE) as db:
        meta = db.get(META, {
            'last_update': datetime.datetime.min,
        })
        if datetime.datetime.now() - meta['last_update'] >= datetime.timedelta(seconds=43200):
            update_all_blocking(db)
            meta['last_update'] = datetime.datetime.now()
            db[META] = meta
        return {
            'data': sorted(
                [{**e.to_dict(), 'key': k}
                 for k, s in db.items() if k != META for e in s if not e.read],
                key=lambda x: x['date']
            ),
        }


def mark_read(key, url):
    with shelve.open(DB_FILE) as db:
        s = db[key]
        s.remove(Entry(url))
        s.add(Entry(url))
        db[key] = s
