"""
Модуль console библиотеки TytyberUtils.
Содержит утилиты для работы с консолью: оформление текста и ASCII-арт.
"""

# Импортируем все необходимое из модуля text_decoration
from .text_decoration import DecorText

# Импортируем все необходимое из модуля symbolText
from .symbolText import print_symbol_text

# Определяем, что будет доступно при импорте модуля console
__all__ = [
    # text_decoration
    'DecorText',
    # symbolText
    'print_symbol_text',
]