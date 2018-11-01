
from flask import Blueprint, request, jsonify

from game.auth import login_required
from game.pc import Player


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/user/<user_id>', methods=('GET'))
def user_get(user_id):
    user = Player(user_id)
    return jsonify(user.data)


@bp.route('/user/<user_id>', methods=('POST'))
@login_required
def user_post(user_id):
    content = request.get_json()
