import csv

import shopping

# a = set()
# with open('shopping.csv', encoding="utf-8") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         a.add(row["Revenue"])
# print(a)

evidence, labels = shopping.load_data('shopping.csv')
for i, j in zip(evidence, labels):
    print(i, j)