"""Versión corregida TP9. Verifica fecha ISO y calendario."""
import re
from datetime import date


def fecha_valida(valor):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor):
        return False
    try:
        date.fromisoformat(valor)
    except ValueError:
        return False
    return True
