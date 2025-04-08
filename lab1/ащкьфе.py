def format_number(value):
    if abs(value) >= 1e4 or (abs(value) < 1e-3 and value != 0):
        return f"{value:.3e}"
    else:
        return str(float(f"{value:.6f}")).rstrip('0').rstrip('.')

for key, value in results.items():
    pearson = format_number(value["pearson"][0])
    spearman = format_number(value["spearman"][0])
    quadrant = format_number(value["quadrant"][0])
    print(f"{key} & {pearson} & {spearman} & {quadrant} \\\\")