import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns

# Генерация выборок разного размера
# %% 1
# Размеры выборок
sizes = [10, 50, 1000]
sqrt = math.sqrt
# Генерация выборок
samples = {
    "Normal": {size: np.random.normal(loc=0, scale=1, size=size) for size in sizes},
    "Cauchy": {size: np.random.standard_cauchy(size=size) for size in sizes},
    "Poisson": {size: np.random.poisson(lam=10, size=size) for size in sizes},
    "Uniform": {size: np.random.uniform(low=-sqrt(3), high=sqrt(3), size=size) for size in sizes}
}

# Визуализация
plt.figure(figsize=(12, 8))

for i, (dist_name, dist_samples) in enumerate(samples.items(), 1):
    plt.subplot(2, 2, i)

    for size, data in dist_samples.items():
        sns.histplot(data, bins=20, kde=True, stat="density", alpha=0.5, label=f"n={size}")

    plt.title(f"{dist_name} Distribution")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)

# Показать графики
plt.tight_layout()
plt.savefig("histograms.png")
plt.show()

# %% 2
import numpy as np
import pandas as pd
from math import sqrt

num_experiments = 1000
sizes = [10, 100, 1000]
distributions = {
    "Нормальное": lambda size: np.random.normal(loc=0, scale=1, size=size),
    "Коши": lambda size: np.random.standard_cauchy(size=size),
    "Пуассон": lambda size: np.random.poisson(lam=10, size=size),
    "Равномерное": lambda size: np.random.uniform(low=-sqrt(3), high=sqrt(3), size=size),
}

# Создаем структуру для хранения результатов
results = {name: {size: {"$\\bar{x}$": [], "$\operatorname{med} x$": [], "$z_Q$": []} for size in sizes} for name in distributions}

# Генерация выборок и расчет статистик
for name, dist_func in distributions.items():
    for size in sizes:
        for _ in range(num_experiments):
            sample = dist_func(size)
            mean_x = np.mean(sample)
            median_x = np.median(sample)
            quartile_mean_x = (np.percentile(sample, 25) + np.percentile(sample, 75)) / 2

            results[name][size]["$\\bar{x}$"].append(mean_x)
            results[name][size]["$\operatorname{med} x$"].append(median_x)
            results[name][size]["$z_Q$"].append(quartile_mean_x)

# Вычисление статистик и формирование таблицы
table = []
for name in distributions:
    for size in sizes:
        for stat_name in ["$\\bar{x}$", "$\operatorname{med} x$", "$z_Q$"]:
            mean_z = np.mean(results[name][size][stat_name])  # E(z)
            mean_z2 = np.mean(np.square(results[name][size][stat_name]))  # E(z^2)
            var_z = mean_z2 - mean_z**2  # D(z)

            table.append([name, size, stat_name, mean_z, var_z])

# Преобразуем в DataFrame
df = pd.DataFrame(table, columns=["Распределение", "Выборка", "характеристика", "E(z)", "D(z)"])

# Формируем таблицу LaTeX
latex_table = df.to_latex(index=False, escape=False, column_format="|c|c|c|c|c|")

print(latex_table)