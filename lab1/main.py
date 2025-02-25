import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Генерация выборок разного размера
sizes = [10, 50, 1000]
samples = {size: np.random.normal(loc=0, scale=1, size=size) for size in sizes}

# Построение графиков
plt.figure(figsize=(10, 6))

for size, data in samples.items():
    sns.histplot(data, bins=30, kde=True, stat="density", alpha=0.5, label=f"n={size}")

# Оформление
plt.xlabel("Value")
plt.ylabel("Density")
plt.title("Histogram and Density for Different Sample Sizes")
plt.legend()
plt.grid(True)

# Показать график
plt.show()

# Количество повторений
num_experiments = 1000
sizes = [10, 100, 1000]

# Хранение результатов
results = {size: {"mean": [], "median": []} for size in sizes}

# Генерация 1000 выборок и расчет характеристик
for size in sizes:
    for _ in range(num_experiments):
        sample = np.random.normal(loc=0, scale=1, size=size)
        mean_x = np.mean(sample)
        median_x = np.median(sample)

        results[size]["mean"].append(mean_x)
        results[size]["median"].append(median_x)

# Вычисление статистик
table = []
for size in sizes:
    mean_x = np.mean(results[size]["mean"])
    mean_x2 = np.mean(np.square(results[size]["mean"]))  # E(mean^2)
    median_x = np.mean(results[size]["median"])
    median_x2 = np.mean(np.square(results[size]["median"]))  # E(median^2)

    # Дисперсии
    var_mean = mean_x2 - mean_x**2
    var_median = median_x2 - median_x**2

    table.append([size, mean_x, var_mean, median_x, var_median])

# Вывод результатов
import pandas as pd
df = pd.DataFrame(table, columns=["Sample Size", "E(mean)", "D(mean)", "E(median)", "D(median)"])
print(df)