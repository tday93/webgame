from game.item import base_inventory
from game.db import get_db, easy_query, json_update


class Player():

    def __init__(self, uid):
        self.uid = uid
        self.db = get_db()
        self.username = None
        self.inventory = None
        self.instantiate()

    def instantiate(self):
        self.inventory = self.get_inventory()
        self.username = self.get_username()
        self.check_inv()

    def check_inv(self):
        if "visible" not in self.inventory:
            self.inventory = base_inventory
            self.store_inventory()
            self.inventory = self.get_inventory()

    def add_good(self, good, qty):
        goods = self.inventory["visible"]["goods"]
        if good in goods:
            goods[good]["qty"] += qty
        else:
            goods[good] = {"qty": qty}

    def get_username(self):
        return easy_query("SELECT username FROM users WHERE id = %s", (self.uid,), self.db)

    def get_inventory(self):
        return easy_query("SELECT inventory FROM users WHERE id = %s", (self.uid,), self.db)["inventory"]

    def store_inventory(self):
            json_update("UPDATE users SET inventory = %s WHERE id = %s", self.inventory, [self.uid])
