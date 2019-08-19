import pandas as pd

df = pd.read_csv('input csv file')
closeness_centralities = df["closeness_centrality"]
max_value = closeness_centralities.max()
df["max_value"] = max_value
df["calculation"] = df ["max_value"] - df["closeness_centrality"]
network_centralization_based = df["calculation"].sum()
print(network_centralization_based)
