import numpy as np

import scipy.stats as stats

np.random.seed(0)  # Для воспроизводимости

# Параметры
alpha = 0.05
n_values = [20, 100]

# Генерация выборок
samples = {n: np.random.normal(loc=0, scale=1, size=n) for n in n_values}


def normal_confidence_intervals(sample, alpha=0.05):
    n = len(sample)
    mean = np.mean(sample)
    std = np.std(sample, ddof=1)

    # ДИ для среднего по t-распределению
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    mean_ci = (mean - t_crit * std / np.sqrt(n), mean + t_crit * std / np.sqrt(n))

    # ДИ для σ по хи-квадрат
    chi2_left = stats.chi2.ppf(1 - alpha / 2, df=n - 1)
    chi2_right = stats.chi2.ppf(alpha / 2, df=n - 1)
    std_ci = (np.sqrt((n - 1) * std ** 2 / chi2_left), np.sqrt((n - 1) * std ** 2 / chi2_right))

    return mean_ci, std_ci


def asymptotic_confidence_intervals(sample, alpha=0.05):
    n = len(sample)
    mean = np.mean(sample)
    std = np.std(sample, ddof=1)

    z_crit = stats.norm.ppf(1 - alpha / 2)

    # ДИ для среднего по ЦПТ
    mean_ci = (mean - z_crit * std / np.sqrt(n), mean + z_crit * std / np.sqrt(n))

    # ДИ для σ — как и для нормального случая (асимптотически)
    chi2_left = stats.chi2.ppf(1 - alpha / 2, df=n - 1)
    chi2_right = stats.chi2.ppf(alpha / 2, df=n - 1)
    std_ci = (np.sqrt((n - 1) * std ** 2 / chi2_left), np.sqrt((n - 1) * std ** 2 / chi2_right))

    return mean_ci, std_ci


def print_table_header(title):
    print(f"\n## {title}")
    print("| $n$ | $m$ | $\\sigma$ |")
    print("|:---:|:-----------------------------:|:-------------------------------:")


def format_interval(interval):
    interval_str = f"{interval[0]:.2f} < x < {interval[1]:.2f}"
    twin_str = f"[[{interval[0]:.2f}, {interval[0]:.2f}], [{interval[1]:.2f}, {interval[1]:.2f}]]"
    return interval_str, twin_str


print_table_header("Доверительные интервалы для параметров нормального распределения")
print("| $n$ | $m$ | $\\sigma$ | $m$ (твин) | $\\sigma$ (твин) |")
print("|:---:|:-----------------------------:|:-------------------------------:|:-----------------------------:|:-------------------------------:|")
for n in n_values:
    m_interval, s_interval = normal_confidence_intervals(samples[n])
    m_str, m_twin = format_interval(m_interval)
    s_str, s_twin = format_interval(s_interval)
    print(f"| {n} | {m_str} | {s_str} | {m_twin} | {s_twin} |")

print_table_header("Доверительные интервалы для параметров произвольного распределения. Асимптотический подход")
print("| $n$ | $m$ | $\\sigma$ | $m$ (твин) | $\\sigma$ (твин) |")
print("|:---:|:-----------------------------:|:-------------------------------:|:-----------------------------:|:-------------------------------:|")
for n in n_values:
    m_interval, s_interval = asymptotic_confidence_intervals(samples[n])
    m_str, m_twin = format_interval(m_interval)
    s_str, s_twin = format_interval(s_interval)
    print(f"| {n} | {m_str} | {s_str} | {m_twin} | {s_twin} |")
