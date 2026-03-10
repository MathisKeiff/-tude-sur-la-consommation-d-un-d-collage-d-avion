import pandas as pd

df = pd.read_parquet("dataset_aircraft1.parquet")
print(df.head())
print(df.shape)