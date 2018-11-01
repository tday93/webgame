import json
from game.db import get_db, easy_query, json_update


class Player():

    def __init__(self, uid):
        self.uid = uid
        self.db = get_db()
        self.username = None
        self.data = None
        self.instantiate()
        self.stats = self.data["stats"]
        self.inv = self.data["inventory"]

    def instantiate(self):
        self.data = self.get_data()
        self.username = self.get_username()
        self.check_data()

    def check_data(self):
        if self.data is None:
            self.data = get_base_data()
            self.store_data()
            self.data = self.get_data()

    def get_username(self):
        return easy_query("SELECT username FROM users WHERE id = %s", (self.uid,), self.db)

    def get_data(self):
        return easy_query("SELECT data FROM users WHERE id = %s", (self.uid,), self.db)["data"]

    def store_data(self):
            json_update("UPDATE users SET data = %s WHERE id = %s", self.data, [self.uid])

    def add_to_stat(self, stat, delta):
        self.stats[stat]["sublevel"] += delta

    def add_to_inventory(self, item):
        pass

    def remove_from_inventory(self, item):
        pass


def get_base_data():
    with open("game/pc_base.json") as fn:
        return json.load(fn)
