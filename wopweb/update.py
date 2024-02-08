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
    print(f"UPDATE DB: {db.db_engine.url}")
    if not abcs:
        abcs = TexnoMagicAlphabets()
        abcs.load()

    print("deleting old data")
    drop_tables()

    print("inserting alphabets:")
    db.init_db()
    for tabc in abcs.abcs['user']:
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
