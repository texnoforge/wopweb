# wopweb

A Flask web app to display and browse all available [Words of Power] alphabets
from [wop.mod.io] mod portal [online][wop].

Comes with a `wopweb` CLI which can export [TexnoMagic] symbols into SVG/PNG
using `cairo`.

status: **alpha**


## online 🌍

See this app online on [wop.texnoforge.dev][wop] 👀


## install

Just install `wopweb` python package from this repo:

```
pip install .
```


## config

Create `wopweb.toml` either in working directory or `/etc/wopweb.toml` for
system-wide config:

```
db = 'sqlite:////var/www/wopweb/db.sqlite'
dynamic_path = '/var/www/wopweb/dynamic'

```

* `db` is a SQLAlchemy database URI
* `dynamic_path` is a writable dir for storing dynamic files such as symbol
  images


## setup

First, get [TexnoMagic] alphabets you want to use.

To download all alphabets from [wop.mod.io] you can use:

```
python3 -m texnomagic.cli download-mods --all
```

To update `wopweb` DB and dynamic files from current [TexnoMagic] alphabets:

```
python3 -m wopweb.cli update
```

To download all alphabets and update in one step:

```
python3 -m wopweb.cli update --get-all
```

You can run the above command periodically to keep in sync with new alphabets.


## dev run

```
FLASK_APP=wopweb FLASK_ENV=development  flask run
```


## deploy

Deploy as any other Flask app. I use `nginx`/`gunicorn`.



[TexnoMagic]: https://texnoforge.github.io/texnomagic/
[Words of Power]: https://texnoforge.dev/words-of-power/
[wop.mod.io]: https://wop.mod.io
[wop]: https://wop.texnoforge.dev
