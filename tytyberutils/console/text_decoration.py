class DecorText:
    # Словари для цветов и стилей
    _COLORS = {
        "red": "31",
        "black": "30", 
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "purple": "35",
        "light_blue": "36",
        "white": "37"
    }
    
    _BACKGROUNDS = {
        "red": "41",
        "black": "40",
        "green": "42", 
        "yellow": "43",
        "blue": "44",
        "purple": "45",
        "light_blue": "46",
        "white": "47"
    }
    
    _STYLES = {
        "bold": "1",
        "italic": "3",
        "underline": "4",
        "strikethrough": "9",
        "reset": "0"
    }
    
    def __init__(self, text, color=None, back_color=None, style=None):
        """
        Инициализация декорированного текста
        
        Args:
            text (str): Текст для форматирования
            color (str): Цвет текста (из _COLORS)
            back_color (str): Цвет фона (из _BACKGROUNDS) 
            style (str или list): Стиль(и) текста (из _STYLES)
        """
        self.text = text
        self.color = color
        self.back_color = back_color
        self.style = style
    
    def paint(self):
        """
        Форматирует текст с помощью ANSI escape-кодов
        """
        codes = []
        
        # Обработка стилей
        if self.style:
            if isinstance(self.style, list):
                for s in self.style:
                    if s in self._STYLES:
                        codes.append(self._STYLES[s])
            elif self.style in self._STYLES:
                codes.append(self._STYLES[self.style])
        
        # Цвет текста
        if self.color and self.color.lower() in self._COLORS:
            codes.append(self._COLORS[self.color.lower()])
        
        # Цвет фона  
        if self.back_color and self.back_color.lower() in self._BACKGROUNDS:
            codes.append(self._BACKGROUNDS[self.back_color.lower()])
        
        # Если есть коды форматирования, применяем их
        if codes:
            # Объединяем коды через точку с запятой
            code_str = ";".join(codes)
            # Возвращаем форматированный текст
            return f"\033[{code_str}m{self.text}\033[0m"
        else:
            # Возвращаем обычный текст без изменений
            return self.text
    
    def __str__(self):
        """Строковое представление объекта"""
        return self.paint()
    
    def __repr__(self):
        """Представление объекта для отладки"""
        return f"DecorText(text='{self.text}', color={self.color}, back_color={self.back_color}, style={self.style})"