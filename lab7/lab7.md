## Определение систематического сдвига в данных

## 1 Постановка задачи

Сгенерировать 2 выборки $X_{1}$ и $X_{2}$ мощностью $n=1000$. Средние и ширины выборок должны отличаться, например

$$
X_{1}=N(0,0.95), \quad X_{2}=N(1,1.05),
$$

где $N(m, \sigma)$ - нормальное распределение.
Для выборок $X_{1}$ и $X_{2}$ найти внутренние и внешние оценки.

$$
\begin{aligned}
\operatorname{Inn} X_{i} & =\left[Q_{1 / 4}, Q_{3 / 4}\right] \\
\text { Out } X_{i} & =\left[\min X_{i}, \max X_{i}\right] .
\end{aligned}
$$

Здесь $Q_{1 / 4}, Q_{3 / 4}$ - первый и третий квартили.
Определить параметр сдвига $a$

$$
X_{1}+a=X_{2}
$$

## 1.1 Метод решения

Варьировать параметр сдвига $a$ и вычислять 2 меры совместности

$$
\begin{aligned}
J_{\text {Inn }} & =\frac{\operatorname{Inn} X_{1} \wedge \operatorname{Inn} X_{2}}{\operatorname{Inn} X_{1} \vee \operatorname{Inn} X_{2}}, \\
J_{\text {Out }} & =\frac{\text { Out } X_{1} \wedge \text { Out } X_{2}}{\text { Out } X_{1} \vee \text { Out } X_{2}},
\end{aligned}
$$

Здесь $J$ - индекс Жаккара, $\wedge, \vee$ - минимум и максимум по включению.
см. https://elib.spbstu.ru/dl/5/tr/2022/tr22-142.pdf/info

## 1.2 Результаты

### 1.2.1

Построить графики $J_{I n n}(a), J_{\text {Inn }}(a)$.

### 1.2.2

Найти оценки

$$
\begin{aligned}
& a_{\text {Inn }}=\arg \max _{a} J_{\text {Inn }}, \\
& a_{\text {Out }}=\arg \max _{a} J_{\text {Out }} .
\end{aligned}
$$
