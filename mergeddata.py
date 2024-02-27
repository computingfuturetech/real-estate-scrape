import pandas as pd

csv_files = ['validated_information2.csv', 'building_information2.csv']

if csv_files:
    print("Found")

dataframes = [pd.read_csv(file) for file in csv_files]
for df_index, df in enumerate(dataframes):
    df.columns = df.columns.str.lower().str.strip()
    print(f"DataFrame {df_index+1} columns:")
    print(df.columns)
    print()
merged_df = pd.merge(dataframes[0], dataframes[1], on='id', how='inner')
merged_df.to_csv('merged_selenium_data.csv', index=False)



