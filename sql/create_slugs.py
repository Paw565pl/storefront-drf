from django.utils.text import slugify

with open("seed_products2.sql", "r") as file:
    lines = file.readlines()

shift = 1
new_lines = lines.copy()
for line_number in range(19, len(lines), 7):
    title = lines[line_number]
    slug = f"'{slugify(title)}',\n"
    new_lines.insert(line_number + shift, slug)
    shift += 1

print(len(lines), len(new_lines))

with open("seed_products.sql", "w") as file:
    file.writelines(new_lines)
