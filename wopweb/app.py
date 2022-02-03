from flask import Flask, abort, render_template, send_from_directory

from wopweb import db
from wopweb.config import cfg
from wopweb import models


db.get_db()
app = Flask(__name__)


@app.route('/')
@app.route('/abcs')
def abcs():
    abcs_ = models.Alphabet.query.all()
    return render_template('abcs.html', abcs=abcs_)


@app.route('/abc/<abc>')
def abc(abc):
    abc_ = models.Alphabet.query.filter(models.Alphabet.handle == abc).first()
    if not abc_:
        abort(404)
    return render_template('abc.html', abc=abc_)


@app.route('/symbol/<abc>/<symbol>')
def symbol(abc, symbol):
    abc_ = models.Alphabet.query.filter(models.Alphabet.handle == abc).first()
    if not abc_:
        abort(404)
    symbols = [s for s in abc_.symbols if s.handle == symbol]
    if not symbols:
        abort(404)
    symbol_ = symbols[0]
    return render_template('symbol.html', symbol=symbol_)


@app.route('/all')
def all_symbols():
    symbols = {}
    for meaning, in db.db_session.query(models.Symbol.meaning).distinct():
        symbols[meaning] = models.Symbol.query.filter(models.Symbol.meaning == meaning).all()
    return render_template('all-symbols.html', symbols=symbols)


@app.route('/dynamic/<path:fn>')
def dynamic(fn):
    return send_from_directory(cfg.dynamic_path, fn)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.close_db()
