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


def open_db():
    return shelve.open('data/store')


def open_meta():
    return shelve.open('data/meta')


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


async def update_all(entries):
    search_entries = [search(**kwargs) for kwargs in entries.values()]
    return await asyncio.gather(*search_entries)


def update_all_blocking(db, meta):
    entries = meta.get('entries', {})
    results = [set(Entry(e) for e in l)
               for l in asyncio.run(update_all(entries))]
    for i, key in enumerate(entries):
        if key not in db:
            db[key] = results[i]
        else:
            db[key] = db[key] | (results[i] - db[key])


def update():
    with open_db() as db:
        with open_meta() as meta:
            update_all_blocking(db, meta)


def fetch():
    with open_db() as db:
        with open_meta() as meta:
            try_update(db, meta)
            return {
                'data': sorted(
                    [{**e.to_dict(), 'key': k}
                     for k in meta.get('entries', {}) for e in db.get(k, []) if not e.read],
                    key=lambda x: x['date'],
                    reverse=True,
                ),
            }


def try_update(db, meta):
    last_update = meta.get('last_update', datetime.datetime.min)
    if datetime.datetime.now() - last_update >= datetime.timedelta(seconds=43200):
        update_all_blocking(db, meta)
        meta['last_update'] = datetime.datetime.now()


def mark_read(key, url):
    with open_db() as db:
        s = db[key]
        s.remove(Entry(url))
        s.add(Entry(url))
        db[key] = s


def add(key, strict):
    with open_meta() as meta:
        entries = meta.get('entries', {})
        if strict == 'true':
            entries[key] = {
                'strict_terms': key,
                'date_range': 3,
            }
        else:
            entries[key] = {
                'keyword': key,
                'date_range': 3,
            }
        meta['entries'] = entries
        with open_db() as db:
            update_all_blocking(db, meta)


def remove(key):
    with open_meta() as meta:
        entries = meta.get('entries', {})
        if key in entries:
            del entries[key]
        meta['entries'] = entries


def ls():
    with open_meta() as meta:
        entries = meta.get('entries', {})
        return [
            {
                'key': key,
                'strict': 'strict_terms' in value,
            } for key, value in entries.items()
        ]
