import matplotlib.pyplot as plt
import numpy as np


# Функции для МНК и МНМ
def MNK(x, y):
    beta1 = (np.mean(x * y) - np.mean(x) * np.mean(y)) / (np.mean(x ** 2) - np.mean(x) ** 2)
    beta0 = np.mean(y) - beta1 * np.mean(x)
    return beta0, beta1


def MNM(x, y):
    med_x = np.median(x)
    med_y = np.median(y)
    sgn = lambda z: np.sign(z)
    rq = np.mean([sgn(xi - med_x) * sgn(yi - med_y) for xi, yi in zip(x, y)])

    def q_star(arr):
        n = len(arr)
        sorted_arr = np.sort(arr)
        l = int(n // 4)
        j = n - l - 1
        kq = 1.491  # k_q(n) для n = 20
        return (sorted_arr[j] - sorted_arr[l]) / kq

    qx_star = q_star(x)
    qy_star = q_star(y)
    beta1r = rq * qy_star / qx_star
    beta0r = med_y - beta1r * med_x
    return beta0r, beta1r


# Генерация данных
np.random.seed(0)
n = 20
x = np.linspace(-1.8, 2, n)
eps = np.random.normal(0, 1, n)
y_clean = 2 + 2 * x + eps
y_perturbed = y_clean.copy()
y_perturbed[0] += 10
y_perturbed[-1] -= 10

# Оценки
methods = ['МНК', 'МНМ']
results_clean = []
results_perturbed = []

for y in [y_clean, y_perturbed]:
    beta0_ls, beta1_ls = MNK(x, y)
    beta0_lm, beta1_lm = MNM(x, y)

    results = [
        ['МНК', beta0_ls, beta0_ls / 2, beta1_ls, beta1_ls / 2],
        ['МНМ', beta0_lm, beta0_lm / 2, beta1_lm, beta1_lm / 2]
    ]
    if np.all(y == y_clean):
        results_clean = results
    else:
        results_perturbed = results


# Функция LaTeX-таблицы
def print_latex_table(data, caption):
    print("\\begin{table}[H]")
    print("\\centering")
    print("\\begin{tabular}{|c|c|c|c|c|c|}")
    print("\\hline")
    print(" & Метод & $\\hat{a}$ & $\\hat{a}/a$ & $\\hat{b}$ & $\\hat{b}/b$ \\\\")
    print("\\hline")
    for i, row in enumerate(data, 1):
        print(f"{i} & {row[0]} & {row[1]:.2f} & {row[2]:.2f} & {row[3]:.2f} & {row[4]:.2f} \\\\")
    print("\\hline")
    print("\\end{tabular}")
    print(f"\\caption{{{caption}}}")
    print("\\end{table}")
    print()


print_latex_table(results_clean, "Оценки коэффициентов регрессии без выбросов")
print_latex_table(results_perturbed, "Оценки коэффициентов регрессии с выбросами")


# Построение графиков
def plot_and_save(x, y, beta0, beta1, beta0_r, beta1_r, title, filename):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='Данные', color='black')
    plt.plot(x, beta0 + beta1 * x, label='МНК', color='blue')
    plt.plot(x, beta0_r + beta1_r * x, label='МНМ', color='red', linestyle='--')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename, dpi=300)
    plt.close()


plot_and_save(x, y_clean, *MNK(x, y_clean), *MNM(x, y_clean),
              "Невозмущённая выборка", "regression_clean.png")

plot_and_save(x, y_perturbed, *MNK(x, y_perturbed), *MNM(x, y_perturbed),
              "Возмущённая выборка", "regression_perturbed.png")
