import functools

from flask import (
    Blueprint, request, redirect, flash, url_for, render_template, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from game.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        db_conn = db["conn"]
        db_cur = db["cur"]
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        db_cur.execute('SELECT id FROM users WHERE username = %s', (username,))
        if db_cur.fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db_cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            db_conn.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        db["cur"].execute('SELECT * FROM users WHERE username = %s', (username,))
        user = db["cur"].fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user["password"], password):
            error = 'Incorrect Password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('user.user_home'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db_cur = get_db()["cur"]

    if user_id is None:
        g.user = None
    else:
        db_cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        g.user = db_cur.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
