import numpy as np
import scipy.stats as stats


# Функция для оценки параметров нормального распределения методом максимального правдоподобия
def estimate_normal_parameters(sample):
    mu_hat = np.mean(sample)
    sigma_hat = np.std(sample, ddof=1)
    return mu_hat, sigma_hat


# Функция для проверки гипотезы с использованием хи-квадрат
def chi_square_test(sample, distribution_type='normal', mu_hat=None, sigma_hat=None):
    n = len(sample)

    k = 6  # количество интервалов
    bins = np.linspace(min(sample), max(sample), k + 1)
    observed_frequencies, _ = np.histogram(sample, bins=bins)

    if distribution_type == 'normal':
        theoretical_probs = [
            stats.norm.cdf(bins[i + 1], loc=mu_hat, scale=sigma_hat) - stats.norm.cdf(bins[i], loc=mu_hat,
                                                                                      scale=sigma_hat) for i in
            range(k)]
        theoretical_frequencies = [p * n for p in theoretical_probs]
    elif distribution_type == 'uniform':
        theoretical_frequencies = [n / k] * k  # равномерная вероятность для каждого интервала

    # Вычисление статистики хи-квадрат
    chi_squared_stat = sum(
        (observed_frequencies[i] - theoretical_frequencies[i]) ** 2 / theoretical_frequencies[i] for i in range(k))
    return chi_squared_stat, observed_frequencies, theoretical_frequencies, bins


np.random.seed(0)
n = 100  # объем выборки
sample_normal = np.random.normal(0, 1, n)

mu_hat, sigma_hat = estimate_normal_parameters(sample_normal)

chi_squared_stat_normal, observed_frequencies_normal, theoretical_frequencies_normal, bins = chi_square_test(
    sample_normal,
    distribution_type='normal',
    mu_hat=mu_hat,
    sigma_hat=sigma_hat)

alpha = 0.05
critical_value_normal = stats.chi2.ppf(1 - alpha, 9)  # k-1 степеней свободы

result_normal = "принимается" if chi_squared_stat_normal < critical_value_normal else "отвергается"

sample_uniform_100 = np.random.uniform(-np.sqrt(3), np.sqrt(3), 100)
sample_uniform_20 = np.random.uniform(-np.sqrt(3), np.sqrt(3), 20)

chi_squared_stat_uniform_100, _, _, _ = chi_square_test(sample_uniform_100, distribution_type='uniform')
chi_squared_stat_uniform_20, _, _, _ = chi_square_test(sample_uniform_20, distribution_type='uniform')

critical_value_uniform = stats.chi2.ppf(1 - alpha, 9)

result_uniform_100 = "отвергается" if chi_squared_stat_uniform_100 >= critical_value_uniform else "принимается"
result_uniform_20 = "отвергается" if chi_squared_stat_uniform_20 >= critical_value_uniform else "принимается"

# Печать результатов
print("Результаты для нормального распределения:")
print(f"Оценка параметра mu: {mu_hat}")
print(f"Оценка параметра sigma: {sigma_hat}")
print(f"Вычисленное значение хи-квадрат для нормального распределения: {chi_squared_stat_normal}")
print(f"Квантиль хи-квадрат для нормального распределения: {critical_value_normal}")
print(f"Гипотеза H0 о нормальном распределении {result_normal}")

print("\nРезультаты для равномерного распределения (100 элементов):")
print(f"Вычисленное значение хи-квадрат для равномерного распределения: {chi_squared_stat_uniform_100}")
print(f"Квантиль хи-квадрат для равномерного распределения: {critical_value_uniform}")
print(f"Гипотеза H0 о равномерном распределении для 100 элементов {result_uniform_100}")
_, observed_frequencies_normal, theoretical_frequencies_normal, bins = chi_square_test(
    sample_uniform_20,
    distribution_type='uniform',
    mu_hat=mu_hat,
    sigma_hat=sigma_hat)
print("\nРезультаты для равномерного распределения (20 элементов):")
print(f"Вычисленное значение хи-квадрат для равномерного распределения: {chi_squared_stat_uniform_20}")
print(f"Квантиль хи-квадрат для равномерного распределения: {critical_value_uniform}")
print(f"Гипотеза H0 о равномерном распределении для 20 элементов {result_uniform_20}")
for i in range(len(bins) - 1):
    print(f"$[{bins[i]:.2f}, {bins[i + 1]:.2f}]$"
          f"&{observed_frequencies_normal[i]}&"
          f"{theoretical_frequencies_normal[i]:.2f}&"
          f"{(observed_frequencies_normal[i] - theoretical_frequencies_normal[i]) ** 2 / theoretical_frequencies_normal[i]:.2f}\\\\")
