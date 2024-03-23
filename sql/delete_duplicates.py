with open("seed_products4.sql", "r") as file:
    lines = file.readlines()

new_lines = lines[0:26]
titles = ["('Bread Ww Cluster',"]
for line_number in range(26, len(lines), 7):
    title = lines[line_number]
    if title in titles:
        continue
    titles.append(title)

    new_lines += lines[line_number : line_number + 7]

with open("seed_products.sql", "w") as file:
    file.writelines(new_lines)
