import pandas as pd

table = pd.read_csv(f"data/final_results/final_csv.csv", encoding="unicode-escape")

print(table.to_html())