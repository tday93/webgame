from flask import render_template, Blueprint
import json

bp = Blueprint('game', __name__, url_prefix="/game")


@bp.route('/')
def game():
    sidenav = get_json("/Users/tday/usr/dev/web_game/game/data/sidenav.json")
    return render_template("game/index.html", sidenav=sidenav)


def get_json(filename):

    with open(filename) as fn:
        json_out = json.load(fn)

    return json_out
