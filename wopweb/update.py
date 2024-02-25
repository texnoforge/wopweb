from texnomagic.abcs import TexnoMagicAlphabets

from wopweb import db
from wopweb.config import cfg
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


def update_db(abcs=None, abcs_tag=None):
    print(f"UPDATE DB: {db.db_engine.url}")
    if not abcs:
        abcs = TexnoMagicAlphabets()
        abcs.load()
    if not abcs_tag:
        abcs_tag = cfg.abcs_tag

    print("deleting old data")
    drop_tables()

    print("inserting alphabets:")
    db.init_db()
    for tabc in abcs.abcs[abcs_tag]:
        print(f"- {tabc}")
        mabc = models.Alphabet(
            name=tabc.name,
            handle=tabc.handle,
        )
        db.db_session.add(mabc)
        for tsymbol in tabc.symbols:
            msymbol = models.Symbol(
                meaning=tsymbol.meaning,
                name=tsymbol.name,
                handle=tsymbol.handle,
                abc=mabc,
            )
            db.db_session.add(msymbol)

    db.db_session.commit()
    return abcs
