from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# فعال‌سازی CORS برای دسترسی از دیگر منابع
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # یا دامنه‌های خاص
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# اتصال به پایگاه داده PostgreSQL
conn = psycopg2.connect(
    dbname="PlayStorDbProject",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# مدل داده‌ای برای اپلیکیشن‌ها
class AppModel(BaseModel):
    app_id: str
    app_name: str
    category_id: int
    rating: float
    rating_count: int
    installs: int
    min_installs: int
    max_installs: int
    free: bool
    price: float
    currency: str
    size: str
    min_android: str
    developer_id: str
    released: str
    last_updated: str
    content_rating: str
    privacy_policy: str
    ad_supported: bool
    in_app_purchases: bool
    editors_choice: bool
class CategoryModel(BaseModel):
    category_name: str
class DeveloperModel(BaseModel):
    developer_id: str
    developer_website: str
    developer_email: str

# (GET) فیلتر کردن اپلیکیشن‌ها بر اساس فیلدهای مختلف
@app.get("/apps/")
def get_apps(
    category_name: str = None, 
    min_rating: float = None,
    max_rating: float = None,
    min_price: float = None,
    max_price: float = None,
    limit: int = 1000
):
    query = """
        SELECT 
            a.AppId, a.AppName, c.CategoryName, a.Rating, a.RatingCount, a.Installs, a.MinInstalls, a.MaxInstalls, a.Free,
            a.Price, a.Currency, a.Size, a.MinAndroid, d.DeveloperId, d.DeveloperWebsite, d.DeveloperEmail, a.Released, a.LastUpdated, a.ContentRating,
            a.PrivacyPolicy, a.AdSupported, a.InAppPurchases, a.EditorsChoice
            
        FROM Apps a
        JOIN Categories c ON a.CategoryId = c.CategoryId
        JOIN Developers d ON a.DeveloperId = d.DeveloperId
        WHERE 1=1
    """    
    # افزودن فیلترها به پرس‌وجو
    if category_name is not None:
        query += f" AND CategoryName = '{category_name}'"
    if min_rating is not None:
        query += f" AND Rating >= {min_rating}"
    if max_rating is not None:
        query += f" AND Rating <= {max_rating}"
    if min_price is not None:
        query += f" AND Price >= {min_price}"
    if max_price is not None:
        query += f" AND Price <= {max_price}"

    # افزودن محدودیت به پرس‌وجو
    query += f" LIMIT {limit};"

    try:
        df = pd.read_sql(query, conn)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# (POST) ایجاد اپلیکیشن جدید
@app.post("/apps/")
def create_app(app: AppModel):
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Apps (AppId, AppName, CategoryId, Rating, RatingCount, Installs, MinInstalls, MaxInstalls, Free,
                              Price, Currency, Size, MinAndroid, DeveloperId, Released, LastUpdated, ContentRating,
                              PrivacyPolicy, AdSupported, InAppPurchases, EditorsChoice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            app.app_id, app.app_name, app.category_id, app.rating, app.rating_count, app.installs,
            app.min_installs, app.max_installs, app.free, app.price, app.currency, app.size,
            app.min_android, app.developer_id, app.released, app.last_updated, app.content_rating,
            app.privacy_policy, app.ad_supported, app.in_app_purchases, app.editors_choice
        ))
        conn.commit()
        return {"message": "App added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

# (PUT) به‌روزرسانی اپلیکیشن موجود
@app.put("/apps/{app_id}")
def update_app(app_id: str, app: AppModel):
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Apps
            SET AppName = %s, CategoryId = %s, Rating = %s, RatingCount = %s, Installs = %s, 
                MinInstalls = %s, MaxInstalls = %s, Free = %s, Price = %s, Currency = %s, Size = %s, 
                MinAndroid = %s, DeveloperId = %s, Released = %s, LastUpdated = %s, ContentRating = %s, 
                PrivacyPolicy = %s, AdSupported = %s, InAppPurchases = %s, EditorsChoice = %s
            WHERE AppId = %s
        """, (
            app.app_name, app.category_id, app.rating, app.rating_count, app.installs,
            app.min_installs, app.max_installs, app.free, app.price, app.currency, app.size,
            app.min_android, app.developer_id, app.released, app.last_updated, app.content_rating,
            app.privacy_policy, app.ad_supported, app.in_app_purchases, app.editors_choice,
            app_id
        ))
        conn.commit()
        return {"message": "App updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

# (DELETE) حذف اپلیکیشن
@app.delete("/apps/{app_id}")
def delete_app(app_id: str):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Apps WHERE AppId = %s", (app_id,))
        conn.commit()
        return {"message": "App deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

# (GET) نمایش میانگین نمرات هر دسته‌بندی
@app.get("/categories/average_ratings/")
def average_rating_per_category():
    query = """
        SELECT 
            c.CategoryName, AVG(a.Rating) AS avg_rating
        FROM Apps a
        JOIN Categories c ON a.CategoryId = c.CategoryId
        GROUP BY c.CategoryName;
    """
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

# (GET) نمودارهای زمانی برای تاریخ‌های Released و LastUpdated
@app.get("/apps/timeline/")
def timeline(category_id: int = None):
    query = """
        SELECT 
            a.AppId, a.AppName, a.Released, a.LastUpdated, c.CategoryName
        FROM Apps a
        JOIN Categories c ON a.CategoryId = c.CategoryId
    """
    if category_id:
        query += f" WHERE a.CategoryId = {category_id}"

    df = pd.read_sql(query, conn)

    # تبدیل تاریخ‌ها به فرمت DateTime برای استفاده در نمودار
    df['released'] = pd.to_datetime(df['released'])
    df['lastupdated'] = pd.to_datetime(df['lastupdated'])

    # آماده‌سازی داده‌ها برای نمودار
    released_per_year = df.groupby(df['released'].dt.year).size()
    last_updated_per_year = df.groupby(df['lastupdated'].dt.year).size()

    # بازگشت داده‌ها برای نمودار
    return {
        "released_per_year": released_per_year.to_dict(),
        "last_updated_per_year": last_updated_per_year.to_dict()
    }

# (GET) نمایش تمام دسته‌بندی‌ها
@app.get("/categories/")
def get_categories():
    query = "SELECT * FROM Categories;"
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

# (POST) ایجاد دسته‌بندی جدید
@app.post("/categories/")
def create_category(category: CategoryModel):
    query = "INSERT INTO Categories (CategoryName) VALUES (%s);"
    cur = conn.cursor()
    try:
        cur.execute(query, (category.category_name,))
        conn.commit()
        return {"message": "Category created successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

# (GET) نمایش تمام توسعه‌دهندگان
@app.get("/developers/")
def get_developers():
    query = "SELECT * FROM Developers;"
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

@app.get("/GetCategoryiD/")
def get_CategoryiD(cat_name: str):
    query = f"SELECT CategoryId FROM Categories where CategoryName = '{cat_name}'"
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")


# (POST) ایجاد توسعه‌دهنده جدید
@app.post("/developers/")
def create_developer(developer: DeveloperModel):
    query = """
        INSERT INTO Developers (DeveloperId, DeveloperWebsite, DeveloperEmail) 
        VALUES (%s, %s, %s);
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (developer.developer_id, developer.developer_website, developer.developer_email))
        conn.commit()
        return {"message": "Developer created successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

# اجرای اپلیکیشن
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

