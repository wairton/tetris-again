import json
import os

from dataclasses import dataclass, asdict
import configuration.config as config


class Controller:

    @dataclass
    class OptionItem:
        Rotate_right: str
        Rotate_left: str
        Down: str
        Left: str
        Right: str
        Ground: str
        Hold: str

    def __init__(self):
        self._data = None
        self._used_keys = []

    def ensure_is_loaded(self):
        if self._data is None:
            self._data = self.load()

    def load(self):
        if os.path.exists(config.OPTIONS_FILE):
            data = json.load(open(config.OPTIONS_FILE))
        else:
            data = self.create_new_control()
        player_list = {}
        for player in data:
            json_values = data[player].values()
            player_list[player] = self.OptionItem(*json_values)
            self._used_keys.append(list(json_values))
        return player_list

    def create_new_control(self):
        file = open(config.OPTIONS_FILE, "x")
        json.dump(
            {"Player1":
             {"Rotate-right": "up", "Rotate-left": "p",
              "Down": "down", "Left": "left",
              "Right": "right", "Ground": "space", "Hold": "h"},
             "Player2":
             {"Rotate-right": "[8]", "Rotate-left": "[7]",
              "Down": "[5]", "Left": "[4]",
              "Right": "[6]", "Ground": "[9]", "Hold": "[1]"}}, file)
        file.close()
        return json.load(open(config.OPTIONS_FILE))

    def is_key_used(self, key_name):
        self.ensure_is_loaded()
        for player in self._used_keys:
            if player.count(key_name) > 0:
                return True
        return False

    def key_change(self, atr, old_key, new_key):
        for player in self._data:
            if getattr(self._data[player], atr) == old_key:
                setattr(self._data[player], atr, new_key)
                break

    def save(self):
        self.ensure_is_loaded()
        save_dict = self._data
        for player in save_dict:
            save_dict[player] = asdict(save_dict[player])
        json.dump(save_dict, open(config.OPTIONS_FILE, "w"))


controller = Controller()
