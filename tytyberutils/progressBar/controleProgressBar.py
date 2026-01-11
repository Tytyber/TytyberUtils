import os
import sys
import time

class ControleBar:
    def __init__(self, operations: int, off_symbol: str = "-", on_symbol: str = "#", step: int = None):
        """
        Контролируемый прогресс-бар
        
        Args:
            operations: Общее количество операций
            off_symbol: Символ для невыполненной части
            on_symbol: Символ для выполненной части
            step: Количество шагов для отображения (если None - определяется автоматически)
        """
        self.operations = operations
        self.off_symbol = off_symbol
        self.on_symbol = on_symbol
        
        # Автоматическое определение количества шагов, если не задано
        if step is None:
            try:
                terminal_width = os.get_terminal_size().columns
                # Оставляем место для процентов и обрамления
                self.step = max(terminal_width - 15, 20)
            except:
                self.step = 50  # Значение по умолчанию
        else:
            self.step = step
            
        # Текущий прогресс (количество выполненных операций)
        self.current = 0
        # Текущая заполненная длина (в символах)
        self.filled_length = 0
        # Процент выполнения
        self.percent = 0
        
    def next_step(self):
        """
        Увеличивает прогресс на одну операцию и обновляет отображение
        
        Returns:
            bool: True если прогресс завершен, False если еще есть шаги
        """
        if self.current >= self.operations:
            return True  # Прогресс уже завершен
            
        # Увеличиваем счетчик
        self.current += 1
        
        # Вычисляем новый процент
        self.percent = min((self.current / self.operations) * 100, 100)
        
        # Вычисляем новую заполненную длину
        new_filled = int((self.current / self.operations) * self.step)
        
        # Обновляем только если изменилось заполнение
        if new_filled != self.filled_length:
            self.filled_length = new_filled
            self._draw()
            
        return self.current >= self.operations
        
    def _draw(self):
        """Отрисовывает текущее состояние прогресс-бара"""
        empty_length = self.step - self.filled_length
        bar = self.on_symbol * self.filled_length + self.off_symbol * empty_length
        
        # Форматируем вывод
        progress_text = f"\r[{bar}] {self.percent:6.2f}% ({self.current}/{self.operations})"
        
        # Выводим
        sys.stdout.write(progress_text)
        sys.stdout.flush()
        
    def finish(self, message: str = "✓ Завершено"):
        """Завершает прогресс-бар с сообщением"""
        # Устанавливаем 100%
        self.current = self.operations
        self.percent = 100
        self.filled_length = self.step
        
        # Отрисовываем завершенное состояние
        self._draw()
        
        # Выводим сообщение на новой строке
        print(f"\n{message}")
        
    def reset(self):
        """Сбрасывает прогресс-бар в начальное состояние"""
        self.current = 0
        self.filled_length = 0
        self.percent = 0
        print()  # Новая строка
        
    def set_progress(self, progress: int):
        """
        Устанавливает конкретное значение прогресса
        
        Args:
            progress: Текущий прогресс (количество выполненных операций)
        """
        if 0 <= progress <= self.operations:
            self.current = progress
            self.percent = min((self.current / self.operations) * 100, 100)
            self.filled_length = int((self.current / self.operations) * self.step)
            self._draw()
        else:
            raise ValueError(f"Прогресс должен быть в диапазоне 0-{self.operations}")
            
    def get_progress(self) -> float:
        """Возвращает текущий процент выполнения"""
        return self.percent


# Расширенная версия с поддержкой цветов и анимации
class EnhancedControleBar(ControleBar):
    def __init__(self, operations: int, off_symbol: str = "░", on_symbol: str = "█", 
                 step: int = None, show_percentage: bool = True, show_count: bool = True,
                 color: str = None, animation: bool = False):
        """
        Улучшенный контролируемый прогресс-бар
        
        Args:
            operations: Общее количество операций
            off_symbol: Символ для невыполненной части
            on_symbol: Символ для выполненной части
            step: Количество шагов для отображения
            show_percentage: Показывать процент выполнения
            show_count: Показывать счетчик операций
            color: Цвет прогресс-бара ('red', 'green', 'blue', 'yellow', 'cyan', 'magenta')
            animation: Включить анимацию (вращающийся символ)
        """
        super().__init__(operations, off_symbol, on_symbol, step)
        self.show_percentage = show_percentage
        self.show_count = show_count
        self.color = color
        self.animation = animation
        self.animation_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.animation_index = 0
        
    def _draw(self):
        """Отрисовывает текущее состояние прогресс-бара с улучшениями"""
        empty_length = self.step - self.filled_length
        bar = self.on_symbol * self.filled_length + self.off_symbol * empty_length
        
        # Добавляем цвет если указан
        if self.color:
            color_codes = {
                'red': '\033[91m',
                'green': '\033[92m',
                'yellow': '\033[93m',
                'blue': '\033[94m',
                'magenta': '\033[95m',
                'cyan': '\033[96m',
            }
            bar = f"{color_codes.get(self.color, '')}{bar}\033[0m"
        
        # Собираем текст
        parts = ["\r["]
        
        # Анимация
        if self.animation and self.current < self.operations:
            parts.append(self.animation_symbols[self.animation_index % len(self.animation_symbols)])
            parts.append(" ")
            self.animation_index += 1
            
        parts.append(f"{bar}]")
        
        # Процент
        if self.show_percentage:
            parts.append(f" {self.percent:6.2f}%")
        
        # Счетчик
        if self.show_count:
            parts.append(f" ({self.current}/{self.operations})")
        
        progress_text = "".join(parts)
        
        # Выводим
        sys.stdout.write(progress_text)
        sys.stdout.flush()
        
    def next_step(self, delay: float = 0):
        """
        Увеличивает прогресс на одну операцию
        
        Args:
            delay: Задержка перед обновлением (для имитации работы)
        """
        if delay > 0:
            time.sleep(delay)
        return super().next_step()