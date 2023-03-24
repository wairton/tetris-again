import json
import os

from dataclasses import dataclass, asdict
import configuration.config as config


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
        if len(self._data) < self.MAX_LENGTH and score > 0:
            return True
        elif score > 0:
            return score > min(self._data, key=lambda k: k.score).score
        return

    def add(self, *, name='___', score=0):
        self.ensure_is_loaded()
        self._data.append(self.ScoreItem(name=name, score=score))

    @property
    def scores(self):
        self.ensure_is_loaded()
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

    def save(self):
        save_list = [asdict(score) for score in self._data]
        json.dump(save_list, open(config.RECORD_FILE, "w"))


highscore = Highscore()
