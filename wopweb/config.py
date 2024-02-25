from pathlib import Path

from dynaconf import Dynaconf, Validator
from platformdirs import PlatformDirs


dirs = PlatformDirs("wopweb", "texnoforge", roaming=True)

CONFIG_FILE = 'wopweb.toml'
DB_FILE = 'wopweb.db'

USER_DATA_PATH = dirs.user_data_path
USER_CONFIG_PATH = dirs.user_config_path / CONFIG_FILE
SITE_CONFIG_PATH = dirs.site_config_path / CONFIG_FILE

SETTINGS_FILES = [Path(CONFIG_FILE), USER_CONFIG_PATH, SITE_CONFIG_PATH]

DEFAULT_DYNAMIC_PATH = USER_DATA_PATH / 'dynamic'
DEFAULT_DB_PATH = USER_DATA_PATH / 'wopweb.db'
DEFAULT_DB = f'sqlite:///{DEFAULT_DB_PATH}'

DEFAULT_ABCS_TAG = 'user'


cfg = Dynaconf(
    envvar_prefix='WOPWEB',
    settings_files=SETTINGS_FILES,
)

cfg.validators.register(
    Validator("db", default=DEFAULT_DB),
    Validator("dynamic_path", default=DEFAULT_DYNAMIC_PATH),
    Validator("abcs_tag", default=DEFAULT_ABCS_TAG),
)

cfg.validators.validate()
