# flake8: noqa
from potluck.settings.base import *

DATABASES["default"]["NAME"] = BASE_DIR / "test_db.sqlite3"
