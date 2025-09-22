from __future__ import annotations

class STM:
    def __init__(self):
        self._d = {}

    def put(self, k, v):
        self._d[k] = v

    def get(self, k, default=None):
        return self._d.get(k, default)

