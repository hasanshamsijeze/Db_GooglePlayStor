import pandas as pd
import numpy as np
filepath=r"D:\university\Esfahan Master\term 1\Advance Database\HW-7-hasan shamsi-4033624011\Google-Playstore.csv";
dataFrame = pd.read_csv(filepath)
duplicates = dataFrame.duplicated().sum()
print(f"Duplicate count: {duplicates}")
if duplicates == 0:
    print("No duplicate data found")
dataFrame.isnull().sum()
dataFrame = dataFrame.dropna(subset=['App Name'])
dataFrame['Rating'].fillna(0, inplace=True)
dataFrame['Rating Count'].fillna(0, inplace=True)
dataFrame['Installs'] = dataFrame['Installs'].astype(str).str.replace(',', '').str.replace('+', '').astype(float)
dataFrame = dataFrame.dropna(subset=['Installs'])
dataFrame = dataFrame.dropna(subset=['Minimum Installs'])
dataFrame['Currency'].fillna('Unknown', inplace=True)
dataFrame['Size'].fillna('Unknown', inplace=True)
dataFrame['Minimum Android'].fillna('Unknown', inplace=True)
dataFrame['Developer Id'].fillna('Unknown', inplace=True)
dataFrame['Developer Email'].fillna('Unknown', inplace=True)
dataFrame['Developer Website'].fillna('Unknown', inplace=True)
dataFrame['Privacy Policy'].fillna('Unknown', inplace=True)
dataFrame['Price'] = dataFrame['Price'].astype(float)
dataFrame['Released'] = pd.to_datetime(df['Released'], errors='coerce')
dataFrame['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
dataFrame['Released'].fillna(pd.to_datetime("2000-01-01"), inplace=True)
dataFrame.to_csv(r"D:\university\Esfahan Master\term 1\Advance Database\HW-7-hasan shamsi-4033624011\ClineGoogle-Playstore.csv", index=False)