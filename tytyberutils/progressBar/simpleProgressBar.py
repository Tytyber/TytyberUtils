import time
import os

def simpleProgress(operations: int, duration: float = 3.0):
    """
    Плавный прогресс-бар с контролируемой длительностью
    
    Args:
        operations: Количество операций
        duration: Общая длительность анимации в секундах
    """
    terminal_size = os.get_terminal_size()
    width = max(terminal_size.columns - 20, 40)  # Ширина прогресс-бара
    
    delay = duration / operations  # Задержка между шагами
    
    print("\nЗагрузка:")
    
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']  # Анимационные символы
    symbol_index = 0
    
    for i in range(operations + 1):
        percent = min((i / operations) * 100, 100)
        filled = int((percent / 100) * width)
        empty = width - filled
        
        # Анимированный символ
        spinner = symbols[symbol_index % len(symbols)]
        symbol_index += 1
        
        # Цветной прогресс-бар
        bar = f"\033[92m{'█' * filled}\033[90m{'░' * empty}\033[0m"
        
        # Формат вывода
        progress = f"{spinner} [{bar}] {percent:5.1f}%"
        
        print(progress, end='\r', flush=True)
        
        if i < operations:
            time.sleep(delay)
    
    print(f"\n✅ Complete {duration:.1f} seconds!")
    