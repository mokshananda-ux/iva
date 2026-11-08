"""Configuración de desarrollo."""
from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# En desarrollo permitimos SQLite para arrancar sin PostgreSQL si hace falta.
import os

if os.environ.get("USE_SQLITE") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
