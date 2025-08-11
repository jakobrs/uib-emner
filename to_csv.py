from types2 import *
import csv

with open("out", "r") as input:
    data = eval(input.read())

data.sort(key = lambda x: x.code)

with open("out.csv", "w") as out:
    writer = csv.writer(out)
    for row in data:
        writer.writerow([row.code, row.title])
