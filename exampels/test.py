import tytyberutils.console as console
import tytyberutils.progressBar as pbar

print(console.DecorText(text="Тестовый текст", color="red", style="bold"))


pbar.simpleProgress(operations=40000)


bar = pbar.EnhancedControleBar(50, color="red", animation=True)
for i in range(50):
    console.print_symbol_text(text="Tytyber", style="standart")
    bar.next_step(delay=0.1)