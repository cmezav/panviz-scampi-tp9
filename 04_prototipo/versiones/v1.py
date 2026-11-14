"""Línea base experimental TP9 con una regla incompleta sembrada."""
import re
from datetime import date


def fecha_valida(valor):
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor))
