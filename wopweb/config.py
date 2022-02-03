from dynaconf import Dynaconf


cfg = Dynaconf(
    envvar_prefix='WOPWEB',
    settings_files=['wopweb.toml', '/etc/wopweb.toml'],
)
