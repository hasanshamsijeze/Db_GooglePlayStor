from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import pandas as pd

app = FastAPI()

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

# (GET) فیلتر کردن اپلیکیشن‌ها بر اساس فیلدهای مختلف
@app.get("/apps/")
def get_apps(
    limit: int = 1000,
    category_id: int = None,
    min_rating: float = None,
    max_rating: float = None,
    min_price: float = None,
    max_price: float = None,
    min_size: float = None,
    max_size: float = None
):
    query = "SELECT * FROM Apps WHERE 1=1"
    
    # افزودن فیلترها به پرس‌وجو
    if category_id is not None:
        query += f" AND CategoryId = {category_id}"
    if min_rating is not None:
        query += f" AND Rating >= {min_rating}"
    if max_rating is not None:
        query += f" AND Rating <= {max_rating}"
    if min_price is not None:
        query += f" AND Price >= {min_price}"
    if max_price is not None:
        query += f" AND Price <= {max_price}"
    if min_size is not None:
        query += f" AND Size >= {min_size}"
    if max_size is not None:
        query += f" AND Size <= {max_size}"

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

# اجرای اپلیکیشن
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
