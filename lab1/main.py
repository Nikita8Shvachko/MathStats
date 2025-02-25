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
import pandas as pd

num_experiments = 1000
sizes = [10, 100, 1000]

results = {size: {"mean": [], "median": [], "quartile_mean": []} for size in sizes}

# Генерация 1000 выборок и расчет статистик
for size in sizes:
    for _ in range(num_experiments):
        sample = np.random.normal(loc=0, scale=1, size=size)  # Используем нормальное распределение
        mean_x = np.mean(sample)
        median_x = np.median(sample)
        quartile_mean_x = (np.percentile(sample, 25) + np.percentile(sample, 75)) / 2

        results[size]["mean"].append(mean_x)
        results[size]["median"].append(median_x)
        results[size]["quartile_mean"].append(quartile_mean_x)

# Вычисление статистик
table = []
for size in sizes:
    for stat_name in ["mean", "median", "quartile_mean"]:
        mean_z = np.mean(results[size][stat_name])  # E(z)
        mean_z2 = np.mean(np.square(results[size][stat_name]))  # E(z^2)
        var_z = mean_z2 - mean_z**2  # D(z)

        table.append([size, stat_name, mean_z, var_z])

# Преобразуем в DataFrame
df = pd.DataFrame(table, columns=["Sample Size", "Statistic", "E(z)", "D(z)"])
print(df)
