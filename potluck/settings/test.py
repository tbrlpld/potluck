from potluck.settings.base import *

DATABASES["default"]["NAME"] = BASE_DIR / "test_db.sqlite3"
