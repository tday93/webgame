from flask import render_template, Blueprint
import json

bp = Blueprint('loc', __name__, url_prefix="/loc")


@bp.route('/')
def game():
    return render_template("location/index.html")


def get_json(filename):

    with open(filename) as fn:
        json_out = json.load(fn)

    return json_out
