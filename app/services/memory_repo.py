# app/services/memory_repo.py

class QuerySet:
    def __init__(self, items):
        self._items = items

    def filter_by(self, **kwargs):
        filtered = [
            item for item in self._items
            if all(getattr(item, k) == v for k, v in kwargs.items())
        ]
        return QuerySet(filtered)

    def first(self):
        return self._items[0] if self._items else None

    def all(self):
        return list(self._items)


class MemoryDB:
    def __init__(self):
        # {'Usuario': [u1, u2, …], 'Tarea': […]} 
        self._storage = {}
        # Contadores para simular autoincrement
        self._counters = {}

    def add(self, obj):
        cls = obj.__class__.__name__
        if cls not in self._storage:
            self._storage[cls] = []
            self._counters[cls] = 1

        # Simula auto-ID
        obj.id = self._counters[cls]
        self._counters[cls] += 1

        self._storage[cls].append(obj)

    def commit(self):
        pass

    def rollback(self):
        pass

    def refresh(self, obj):
        pass

    def query(self, model):
        cls = model.__name__
        items = self._storage.get(cls, [])
        return QuerySet(items)
