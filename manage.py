#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para el proyecto IVA."""
import os
import sys


def main() -> None:
    # Por defecto usamos la configuración de desarrollo.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y activado el "
            "entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
