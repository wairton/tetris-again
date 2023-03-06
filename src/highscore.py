import json
import os

from dataclasses import dataclass
import config


class Highscore:
    MAX_LENGTH = 10

    @dataclass
    class ScoreItem:
        name: str
        score: int

    def __init__(self):
        self._data = None

    def is_highscore(self, score):
        self.ensure_is_loaded()
        if len(self._data) < self.MAX_LENGTH:
            return True
        else:
            return score > min(self._data, key=lambda k: k.score)

    def add(self, *, name='___', score=0):
        self.ensure_is_loaded()
        self._data.append(self.ScoreItem(name=name, score=score))

    @property
    def scores(self):
        if self._data is None:
            self._data = self.load()
        return sorted(self._data[:], reverse=True, key=lambda s: s.score)

    def ensure_is_loaded(self):
        if self._data is None:
            self._data = self.load()

    def load(self):
        if os.path.exists(config.RECORD_FILE):
            data = json.load(open(config.RECORD_FILE))
        else:
            data = []
        return [self.ScoreItem(**item) for item in data]

    def dump(self):
        dump = json.dumps(self._data, default=self.object_to_dict)
        with open(config.RECORD_FILE, "w") as f:
            f.write(dump)
        return "Worked!"

    def object_to_dict(self, data):
        if isinstance(data, self.ScoreItem):
            return ({"name": data.name, "score": data.score})


highscore = Highscore()
