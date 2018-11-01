from flask import Blueprint, g, render_template

from game.auth import login_required
from game.pc import Player

from game.base_info import sidenav


bp = Blueprint('user', __name__, url_prefix='/user')


# stats
@bp.route('/stats')
@login_required
def stats():
    pc = Player(g.user["id"])
    return render_template("game/stats.html", pc=pc, sidenav=sidenav)

# inventory


# journal
