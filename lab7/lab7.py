import matplotlib.pyplot as plt
import numpy as np

# Генерация выборок
np.random.seed(42)
n = 1000
X1 = np.random.normal(loc=0, scale=0.95, size=n)
X2 = np.random.normal(loc=1, scale=1.05, size=n)


# Внутренний и внешний интервалы
def inner_interval(x):
    q1, q3 = np.percentile(x, [25, 75])
    return q1, q3


def outer_interval(x):
    return np.min(x), np.max(x)


# Индекс Жаккара для двух интервалов
def jaccard_index(interval1, interval2):
    a1, b1 = interval1
    a2, b2 = interval2
    inter = max(0, min(b1, b2) - max(a1, a2))  # длина пересечения
    union = max(b1, b2) - min(a1, a2)  # длина объединения
    return inter / union if union > 0 else 0


# Перебор значений сдвига a
a_values = np.linspace(-2, 4, 300)
j_inn = []
j_out = []

inn2 = inner_interval(X2)
out2 = outer_interval(X2)

for a in a_values:
    X1_shifted = X1 + a
    inn1 = inner_interval(X1_shifted)
    out1 = outer_interval(X1_shifted)
    j_inn.append(jaccard_index(inn1, inn2))
    j_out.append(jaccard_index(out1, out2))

# Нахождение оценок сдвига
a_inn = a_values[np.argmax(j_inn)]  # Оценка сдвига для внутреннего интервала
a_out = a_values[np.argmax(j_out)]  # Оценка сдвига для внешнего интервала

# Вывод результатов
print(f'Оценка сдвига для внутреннего интервала: a_inn ≈ {a_inn:.2f}')
print(f'Оценка сдвига для внешнего интервала: a_out ≈ {a_out:.2f}')

# Визуализация
plt.figure(figsize=(10, 5))
plt.plot(a_values, j_inn, label='J_inn(a)')
plt.plot(a_values, j_out, label='J_out(a)')
plt.axvline(a_inn, color='blue', linestyle='--', label=f'a_inn ≈ {a_inn:.2f}')
plt.axvline(a_out, color='orange', linestyle='--', label=f'a_out ≈ {a_out:.2f}')
plt.xlabel('a')
plt.ylabel('Jaccard Index')
plt.title('Индексы Жаккара в зависимости от сдвига a')
plt.legend()
plt.grid(True)
plt.show()
