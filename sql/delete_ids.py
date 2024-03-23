from re import sub as re_sub

with open("seed_products.sql", "r") as file:
    lines = file.readlines()

for line_number in range(26, len(lines), 8):
    item_id = lines[line_number]
    new_item_id = re_sub(r"\d+,", "", item_id)
    lines[line_number] = new_item_id

with open("seed_products4.sql", "w") as file:
    file.writelines(lines)
