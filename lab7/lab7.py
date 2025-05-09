import matplotlib.pyplot as plt
import numpy as np

class TwinInterval:
    """
    Класс для представления твина (двойного интервала)
    X = [a,b] = [[a,a],[b,b]]
    """
    def __init__(self, a, b):
        self.a = a  # левый конец интервала
        self.b = b  # правый конец интервала

    def __str__(self):
        return f"[[{self.a:.3f}, {self.a:.3f}], [{self.b:.3f}, {self.b:.3f}]]"

    def length(self):
        """Длина интервала"""
        return self.b - self.a

    def center(self):
        """Центр интервала"""
        return (self.a + self.b) / 2

    def contains(self, other):
        """Проверка включения интервала (⊆)"""
        return self.a <= other.a and self.b >= other.b

    def less_or_equal(self, other):
        """Проверка отношения ≤"""
        return self.b <= other.a

# Генерация выборок
np.random.seed(42)
n = 1000
X1 = np.random.normal(loc=0, scale=0.95, size=n)
X2 = np.random.normal(loc=1, scale=1.05, size=n)

# Вывод статистических характеристик исходных выборок
print("Статистические характеристики исходных выборок:")
print(f"X1: mean = {np.mean(X1):.3f}, std = {np.std(X1):.3f}")
print(f"X2: mean = {np.mean(X2):.3f}, std = {np.std(X2):.3f}")
print(f"Теоретическая разница средних: {1.0:.3f}\n")

def create_twin_intervals(x):
    """
    Создает твины для выборки x:
    - внутренний твин (25% и 75% квантили)
    - внешний твин (минимум и максимум)
    """
    q1, q3 = np.percentile(x, [25, 75])
    min_val, max_val = np.min(x), np.max(x)
    return TwinInterval(q1, q3), TwinInterval(min_val, max_val)

def jaccard_index_twin(twin1, twin2):
    """
    Вычисляет индекс Жаккара для двух твинов
    """
    inter = max(0, min(twin1.b, twin2.b) - max(twin1.a, twin2.a))
    union = max(twin1.b, twin2.b) - min(twin1.a, twin2.a)
    return inter / union if union > 0 else 0

# Создаем твины для X2
inn2, out2 = create_twin_intervals(X2)

# Вывод информации о твинах X2
print("Твины для выборки X2:")
print(f"Внутренний твин: {inn2}")
print(f"Длина внутреннего твина: {inn2.length():.3f}")
print(f"Центр внутреннего твина: {inn2.center():.3f}")
print(f"Внешний твин: {out2}")
print(f"Длина внешнего твина: {out2.length():.3f}")
print(f"Центр внешнего твина: {out2.center():.3f}\n")

# Перебор значений сдвига a
a_values = np.linspace(-2, 4, 300)
j_inn = []
j_out = []

for a in a_values:
    X1_shifted = X1 + a
    inn1, out1 = create_twin_intervals(X1_shifted)
    j_inn.append(jaccard_index_twin(inn1, inn2))
    j_out.append(jaccard_index_twin(out1, out2))

# Нахождение оценок сдвига
a_inn = a_values[np.argmax(j_inn)]
a_out = a_values[np.argmax(j_out)]

# Создаем твины для X1 с оптимальным сдвигом
X1_shifted_inn = X1 + a_inn
X1_shifted_out = X1 + a_out
inn1_opt, _ = create_twin_intervals(X1_shifted_inn)
_, out1_opt = create_twin_intervals(X1_shifted_out)

# Вывод результатов
print("Результаты анализа:")
print(f"Оценка сдвига для внутреннего твина: a_inn ≈ {a_inn:.3f}")
print(f"Оценка сдвига для внешнего твина: a_out ≈ {a_out:.3f}")
print(f"Отклонение от теоретического значения (1.0):")
print(f"Для внутреннего твина: {abs(a_inn - 1.0):.3f}")
print(f"Для внешнего твина: {abs(a_out - 1.0):.3f}\n")

print("Твины при оптимальном сдвиге:")
print("Внутренние твины:")
print(f"X1 (со сдвигом {a_inn:.3f}): {inn1_opt}")
print(f"X2: {inn2}")
print(f"Индекс Жаккара: {jaccard_index_twin(inn1_opt, inn2):.3f}\n")

print("Внешние твины:")
print(f"X1 (со сдвигом {a_out:.3f}): {out1_opt}")
print(f"X2: {out2}")
print(f"Индекс Жаккара: {jaccard_index_twin(out1_opt, out2):.3f}")

# Визуализация
plt.figure(figsize=(12, 5))

# График индексов Жаккара
plt.subplot(1, 2, 1)
plt.plot(a_values, j_inn, label='J_inn(a)')
plt.plot(a_values, j_out, label='J_out(a)')
plt.axvline(a_inn, color='blue', linestyle='--', label=f'a_inn ≈ {a_inn:.3f}')
plt.axvline(a_out, color='orange', linestyle='--', label=f'a_out ≈ {a_out:.3f}')
plt.axvline(1.0, color='red', linestyle=':', label='Теоретическое значение (1.0)')
plt.xlabel('a')
plt.ylabel('Jaccard Index')
plt.title('Индексы Жаккара в зависимости от сдвига a')
plt.legend()
plt.grid(True)

# График твинов
plt.subplot(1, 2, 2)
x = np.linspace(-3, 4, 1000)
plt.hist(X1, bins=50, alpha=0.5, label='X1', density=True)
plt.hist(X2, bins=50, alpha=0.5, label='X2', density=True)

# Отображение твинов
plt.axvspan(inn2.a, inn2.b, alpha=0.2, color='blue', label='Внутренний твин X2')
plt.axvspan(out2.a, out2.b, alpha=0.1, color='orange', label='Внешний твин X2')

# Отображение центров твинов
plt.axvline(inn2.center(), color='blue', linestyle=':', label='Центр внутр. твина')
plt.axvline(out2.center(), color='orange', linestyle=':', label='Центр внеш. твина')

plt.xlabel('Значение')
plt.ylabel('Плотность')
plt.title('Распределение выборок и их твины')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('lab7/plot.png', dpi=300, bbox_inches='tight')
plt.show()
