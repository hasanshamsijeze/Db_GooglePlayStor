import pandas as pd
import pyodbc
    
# خواندن فایل CSV
df = pd.read_csv("Google-Playstore.csv")

# اتصال به SQL Server
conn = pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=Google Playstore;Trusted_Connection=yes;")
cursor = conn.cursor()

# وارد کردن داده‌ها به جدول Apps

for index, row in df.iterrows():
    print(index)
   # if(index ==0):
    #    continue
    print(row["App Name"])
    cursor.execute("""
        INSERT INTO Apps (AppName, AppId, Category, Rating, RatingCount, Installs, 
                          MinimumInstalls, MaximumInstalls, Free, Price, Currency, 
                          Size, MinimumAndroid, DeveloperId, DeveloperWebsite, 
                          DeveloperEmail, Released, LastUpdated, ContentRating, 
                          PrivacyPolicy, AdSupported, InAppPurchases, EditorsChoice, ScrapedTime)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row.AppName, row.AppId, row.Category, row.Rating, row.RatingCount, row.Installs,
         row.MinimumInstalls, row.MaximumInstalls, row.Free, row.Price, row.Currency,
         row.Size, row.MinimumAndroid, row.DeveloperId, row.DeveloperWebsite,
         row.DeveloperEmail, row.Released, row.LastUpdated, row.ContentRating,
         row.PrivacyPolicy, row.AdSupported, row.InAppPurchases, row.EditorsChoice, row.ScrapedTime)

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
