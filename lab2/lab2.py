import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Определение распределений
distributions = [
    {"name": "Normal", "dist": np.random.normal, "args": (0, 1)},
    {"name": "Cauchy", "dist": np.random.standard_cauchy, "args": ()},
    {"name": "Poisson", "dist": np.random.poisson, "args": (10,)},
    {"name": "Uniform", "dist": np.random.uniform, "args": (-np.sqrt(3), np.sqrt(3))}
]

sizes = [20, 100, 1000]
outliers_count = []

for distribution in distributions:
    fig, ax = plt.subplots(figsize=(10, 5))
    samples = [distribution["dist"](*distribution["args"], size=size) for size in sizes]

    ax.boxplot(
        samples, positions=[1, 2, 3], widths=0.6, patch_artist=True,
        showfliers=True, flierprops={'markerfacecolor': 'r', 'marker': 'o'}
    )

    # Подсчёт выбросов
    dist_outliers = []
    for sample in samples:
        q1, q3 = np.percentile(sample, [25, 75])
        iqr = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = np.sum((sample < lower_bound) | (sample > upper_bound))  # Векторизованный подсчёт
        dist_outliers.append(outliers)

    outliers_count.append([distribution["name"]] + dist_outliers)

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(sizes)
    ax.set_title(f'Boxplot for {distribution["name"]} Distribution')
    ax.set_xlabel("Sample Size")
    ax.set_ylabel("Values")

    # Сохранение графика
    plot_path = os.path.join(output_dir, f"{distribution['name'].lower()}_boxplot.png")
    plt.savefig(plot_path, dpi=300)
    plt.close(fig)  # Закрытие фигуры после сохранения

# Таблица с числом выбросов
df = pd.DataFrame(outliers_count, columns=["Distribution"] + [f"n={size}" for size in sizes])
print(df)
