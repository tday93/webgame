from flask import Blueprint, g, render_template

from game.auth import login_required
from game.pc import Player


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@login_required
def user_home():
    pc = Player(g.user["id"])
    return render_template("game/user.html", pc=pc)


@bp.route('add_good')
def add_good():
    pass
