import pandas as pd
lines = []

with open('nasdaqtraded.csv') as f:
    lines = f.readlines()
    for i in range(0, len(lines) - 1):
        lines[i + 1] = str(i) + "|" + lines[i + 1]

with open('nasdaqtraded2.csv', 'w') as f:
    for i in range(0, len(lines)):
        f.write(lines[i])
    