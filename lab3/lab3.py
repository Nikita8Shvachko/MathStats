import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib.patches import Ellipse

# Параметры
sizes = [20, 60, 100]
rhos = [0, 0.5, 0.9]
n_trials = 1000
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)


def generate_bivariate_normal(size, rho):
    mean = [0, 0]
    cov = [[1, rho], [rho, 1]]
    return np.random.multivariate_normal(mean, cov, size)


def generate_mixture_normal(size):
    samples = []
    for _ in range(size):
        if np.random.rand() < 0.9:
            samples.append(np.random.multivariate_normal([0, 0], [[1, 0.9], [0.9, 1]]))
        else:
            samples.append(np.random.multivariate_normal([0, 0], [[10, -0.9], [-0.9, 10]]))
    return np.array(samples)


def compute_statistics(samples):
    pearson_corr = []
    spearman_corr = []
    quadrant_corr = []

    for _ in range(n_trials):
        sample = samples[np.random.choice(samples.shape[0], len(samples), replace=True)]
        x, y = sample[:, 0], sample[:, 1]

        pearson_corr.append(stats.pearsonr(x, y)[0])
        spearman_corr.append(stats.spearmanr(x, y)[0])
        quadrant_corr.append(np.sign(x * y).mean())

    return {
        "pearson": (np.mean(pearson_corr), np.mean(np.square(pearson_corr)), np.var(pearson_corr)),
        "spearman": (np.mean(spearman_corr), np.mean(np.square(spearman_corr)), np.var(spearman_corr)),
        "quadrant": (np.mean(quadrant_corr), np.mean(np.square(quadrant_corr)), np.var(quadrant_corr)),
    }


def plot_samples(samples, rho, size, distribution_name):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(samples[:, 0], samples[:, 1], alpha=0.5, s=10)

    # Эллипс равновероятности
    cov = np.cov(samples, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * np.sqrt(vals)
    ellipse = Ellipse(xy=(0, 0), width=width, height=height, angle=angle, edgecolor='r', facecolor='none')
    ax.add_patch(ellipse)

    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_title(f'{distribution_name} (rho={rho}, n={size})')

    plt.savefig(os.path.join(output_dir, f'{distribution_name.lower()}_rho{rho}_n{size}.png'))
    plt.close(fig)


# Основной цикл для нормального распределения
results = {}
true_rhos = {}
for rho in rhos:
    for size in sizes:
        samples = generate_bivariate_normal(size, rho)
        stats_result = compute_statistics(samples)
        actual_rho = np.corrcoef(samples[:, 0], samples[:, 1])[0, 1]

        results[("Normal", rho, size)] = stats_result
        true_rhos[("Normal", rho, size)] = actual_rho

        plot_samples(samples, rho, size, "Normal")

# Основной цикл для смеси нормальных распределений
for size in sizes:
    samples = generate_mixture_normal(size)
    stats_result = compute_statistics(samples)
    actual_rho = np.corrcoef(samples[:, 0], samples[:, 1])[0, 1]

    results[("Mixture", "", size)] = stats_result
    true_rhos[("Mixture", "", size)] = actual_rho

    plot_samples(samples, "Mixture", size, "Mixture")

# Вывод результатов с фактической корреляцией
for key, value in results.items():
    expected_rho = key[1] if key[0] == "Normal" else "mixture"
    actual_rho = true_rhos[key]
    print(f'{key} &  {actual_rho:.2f} & '
          f' {value["pearson"][0]:.2f} & '
          f' {value["spearman"][0]:.2f} & '
          f' {value["quadrant"][0]:.2f} \\\\')
