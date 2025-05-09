Линейная регрессия матстат лаба 4 занятие 26.03

Востановление зависимостей

Входные данные (x_i, y_i)

Модель y = f(beta, x)
beta - параметр

(y_i, x_i)-> beta = ?

Q = sum i=1 to n (y_i - beta_0 - beta_1 * x_i )^2

Метод наименьших квадратов:

Q -> min для beta_1 beta_2
ß_0, ß_1 = arg [ Q -> min для beta_1 beta_2]

**Преимущества**:
теоретически: оптимальность, вычисляется по формулам

**Недостатки**:
неустойчив к аномалиям(выбросам)

Q - квадратная формула
Q = ∑∆_i ^2 - > max ∆_i^2

$$
\left\{\begin{array} { l }
{ \frac { \partial Q } { \partial \beta _ { 0 } } = 0 } \\
{ \frac { \partial Q } { \partial \beta _ { 1 } } = 0 }
\end{array} \Rightarrow \left\{\left.\begin{array}{l}
\hat{\beta}_0+\bar{x} \hat{\beta}_1=\bar{y} \\
\bar{x} \beta_0+\bar{x}^2 \beta_1=x_y
\end{array} \right\rvert\, =>\right.\right.
$$

$$
\begin{aligned}
& \hat{\beta}_1=\frac{\overline{x y}-\bar{x} \cdot \bar{y}}{\overline{x^2}-(\bar{x})^2} \\
& \hat{\beta}_0=\bar{y}-\left.\bar{x}\right| {\beta_1}
\end{aligned}
$$


