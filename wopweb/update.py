from texnomagic.abcs import TexnoMagicAlphabets

from wopweb import db
from wopweb import models


def drop_tables():
    try:
        models.Alphabet.__table__.drop(db.db_engine)
    except Exception:
        pass
    try:
        models.Symbol.__table__.drop(db.db_engine)
    except Exception:
        pass

    # To delete all rows instead:
    # models.Alphabet.query.delete()


def update_db(abcs=None):
    print("updating WoP DB...")
    if not abcs:
        abcs = TexnoMagicAlphabets()
        abcs.load()

    print("deleting old data...")
    drop_tables()

    print("populating DB...")
    db.init_db()
    for tabc in abcs.abcs['mods']:
        print(tabc)
        mabc = models.Alphabet(
            name=tabc.name,
            handle=tabc.handle)
        db.db_session.add(mabc)
        for tsymbol in tabc.symbols:
            msymbol = models.Symbol(
                name=tsymbol.name,
                handle=tsymbol.handle,
                meaning=tsymbol.meaning,
                abc=mabc)
            db.db_session.add(msymbol)

    db.db_session.commit()
    return abcs
