import os
from unittest.mock import patch

from django.test import SimpleTestCase


class DatabaseConfigurationTests(SimpleTestCase):
    def test_defaults_to_sqlite_when_no_database_env_is_set(self):
        for key in [
            'DATABASE_URL',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_PORT',
        ]:
            os.environ.pop(key, None)

        with patch.dict(os.environ, {}, clear=False):
            from minor import settings as settings_module

            config = settings_module.get_database_config()

            self.assertEqual(config['ENGINE'], 'django.db.backends.sqlite3')
            self.assertEqual(config['NAME'], str(settings_module.BASE_DIR / 'db.sqlite3'))
