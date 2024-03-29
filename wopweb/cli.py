"""
wopweb CLI
"""
import sys
import webbrowser

import click
import toml

from texnomagic.abcs import TexnoMagicAlphabets

from wopweb import __version__
from wopweb import db as db_mod
from wopweb import draw
from wopweb import mods
from wopweb import update as update_
from wopweb import server as server_mod
from wopweb import config as config_mod
from wopweb.config import cfg


CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}


def required_option(option):
    val = cfg.get(option)
    if val:
        return val
    raise click.ClickException("Missing required config option: %s" % option)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, message='%(version)s',
                      help="Show wopweb version and exit.")
@click.option('-c', '--config', type=click.Path(exists=True, dir_okay=False),
              help='wopweb config file [default: /etc/wopweb.toml]')
def cli(config):
    """
    Words of Power web tool
    """
    if config:
        cfg.load_file(path=config)


@cli.command(name='config')
def config():
    """
    Show wopweb config.
    """
    print("wopweb config files:")
    for settings_file in config_mod.SETTINGS_FILES:
        if settings_file.exists():
            state = "exists"
        else:
            state = "doesn't exist"
        print(f"- {settings_file} {state}")

    print("\nEFFECTIVE CONFIG:\n")
    print(toml.dumps(cfg.as_dict()))


@cli.command(name="update")
@click.option('-g', '--get-all', is_flag=True,
              help='Download all Words of Power alphabets first.')
def update_all(get_all=False):
    """
    Update WoP database and generate dynamic files (images).
    """
    if get_all:
        mods.download_all_mods()

    db_mod.get_db(cfg.db)
    abcs = draw.draw_images(cfg.dynamic_path)
    print()
    update_.update_db(abcs)
    db_mod.close_db()


@cli.command()
def update_db():
    """
    Update WoP database with current TexnoMagic alphabets.
    """
    db_mod.get_db(cfg.db)
    update_.update_db()
    db_mod.close_db()


@cli.command()
def update_images():
    """
    Generate symbol image files from TexnoMagic alphabets.
    """
    draw.draw_images(cfg.dynamic_path)


@cli.command()
@click.option('-p', '--port', type=int,
              default = server_mod.PORT_DEFAULT, show_default=True,
              help="Run on specified port.")
@click.option('-d', '--debug', is_flag=True,
              help="Debug server.")
@click.option('-o', '--open', is_flag=True,
              help="Open server in web browser.")
@click.option('-u', '--update', is_flag=True,
              help="Update db and images first.")
def server(port, debug, open, update):
    """
    Run local wopweb server.
    """
    if update:
        # update db and dynamic first
        update_all.callback()
        print()

    if open:
        # open browser first
        url = f'http://localhost:{port}/'
        print(f"Opening web browser: {url}")
        webbrowser.open(url)

    server_mod.app.run(host='0.0.0.0', port=port, debug=debug)


@cli.command()
@click.argument('abc')
@click.argument('symbol')
@click.argument('outfile', type=click.Path())
@click.option('-f', '--format', type=click.Choice(['svg', 'png']), default='svg',
              help="output format")
def draw_symbol(abc, symbol, format='svg', outfile=None):
    """
    Draw a TexnoMagic symbol as SVG or PNG image.
    """
    print(f"DRAW SYMBOL {abc}/{symbol} -> {outfile} ({format})")
    abcs = TexnoMagicAlphabets()
    abcs.load()
    tabc = abcs.get_alphabet(abc)
    if not tabc:
        print("ERROR: TexnoMagic alphabet not found: %s" % abc)
        sys.exit(42)
    tsymbol = tabc.get_symbol(symbol)
    if not tsymbol:
        print("ERROR: TexnoMagic symbol not found: %s" % symbol)
        sys.exit(43)

    if outfile == '-':
        outfile = sys.stdout.buffer
    draw.draw_symbol(tsymbol, outfile, format=format)


def main():
    cli()


if __name__ == '__main__':
    main()
