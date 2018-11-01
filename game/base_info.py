import json


def get_json(filepath):

    with open(filepath) as fn:
        return json.load(fn)


sidenav = get_json("game/content/sidenav.json")
