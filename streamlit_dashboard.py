import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

# آدرس API FastAPI شما
API_URL = "http://127.0.0.1:8000"
def fetch_categories():
    response = requests.get(API_URL+"/categories/")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data: {response.text}")
        return pd.DataFrame()
    
def fetch_average_ratings():
    response = requests.get(API_URL+"/categories/average_ratings/")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data: {response.text}")
        return pd.DataFrame()
    
# تابع برای ارسال درخواست به API و دریافت داده‌ها
def fetch_apps(category_id=None, min_rating=None, max_rating=None, min_price=None, max_price=None,limit=1000):
    params = {
        "category_id": category_id,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_price": min_price,
        "max_price": max_price,
        "limit": limit
    }
    response = requests.get(API_URL+"/apps/", params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data: {response.text}")
        return pd.DataFrame()

def fetch_timeline(category_id=None):
    params = {
        "category_id": category_id
    }
    response = requests.get(API_URL+"/apps/timeline/", params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data: {response.text}")
        return pd.DataFrame()

def fetch_timeline(category_id=None):
    params = {
        "category_id": category_id
    }
    response = requests.get(API_URL+"/apps/timeline/", params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data: {response.text}")
        return pd.DataFrame()

def getCategoryId(category_name):
    params = {
        "cat_name": category_name
    }
    response = requests.get(API_URL+"/GetCategoryiD/", params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return None
    
# تنظیمات استریم‌لیت
st.title("Play Store App Dashboard")

# فیلترهای ورودی
st.sidebar.header("فیلترها")
categoriesJson = fetch_categories()
category_options = categoriesJson['categoryname'].tolist()


category_options.insert(0, 'همه دسته‌ها')  # افزودن گزینه برای همه دسته‌ها
category_name = st.sidebar.selectbox("دسته‌بندی", options=category_options)

# یافتن CategoryId بر اساس نام دسته‌بندی انتخابی
category_id = None
if category_name == 'همه دسته‌ها':
    category_id = None
else :
    category_id = category_name

min_rating = st.sidebar.slider("حداقل امتیاز", 0.0, 5.0, 0.0)
max_rating = st.sidebar.slider("حداکثر امتیاز", 0.0, 5.0, 5.0)
min_price = st.sidebar.number_input("حداقل قیمت", min_value=0.0, value=0.0)
max_price = st.sidebar.number_input("حداکثر قیمت", min_value=0.0, value=100.0)
limit = st.sidebar.slider("حداکثر تعداد نتایج", 1, 1000, 100)

# دریافت داده‌ها از API
data = fetch_apps(category_id, min_rating, max_rating, min_price, max_price, limit)

# نمایش داده‌ها در داشبورد
if not data.empty:
    st.write(f"تعداد اپلیکیشن‌های پیدا شده: {len(data)}")
    
    # نمایش جدول داده‌ها
    st.dataframe(data)

else:
    st.write("هیچ داده‌ای برای نمایش یافت نشد.")


# رسم نمودار امتیاز در برابر قیمت
st.subheader("average ratings on each category")
fig, ax = plt.subplots()
avList = fetch_average_ratings()
ax.bar(avList['categoryname'], avList['avg_rating'], alpha=0.8)
ax.set_xlabel("categoryName")
ax.set_ylabel("avg_rating")
plt.xticks(rotation=-90, fontsize=5)  # تغییر اندازه نوشته‌های محور افقی

st.pyplot(fig)



if category_id is not None:
    catId =getCategoryId(category_id)['categoryid'][0]
else:
    catId = None


# نمودار تعداد نصب‌ها در برابر دسته‌بندی
st.subheader(f"تعداد نسخه نهایی در هر سال({category_name})")
avList = fetch_timeline(catId)
pyr =  avList['released_per_year']
sorted_pyr = dict(sorted(pyr.items()))
keys_list = list(sorted_pyr.keys())
values_list = list(sorted_pyr.values())
fig2, ax2 = plt.subplots()
ax2.bar(keys_list, values_list, alpha=0.8)
ax2.set_xlabel("year")
ax2.set_ylabel("count")
plt.xticks(rotation=-90, fontsize=10)  # تغییر اندازه نوشته‌های محور افقی
st.pyplot(fig2)

# نمودار تعداد نصب‌ها در برابر دسته‌بندی
st.subheader(f"آخرین ویؤایش در هر سال({category_name})")
pyr =  avList['last_updated_per_year']
sorted_pyr = dict(sorted(pyr.items()))
keys_list = list(sorted_pyr.keys())
values_list = list(sorted_pyr.values())
fig3, ax3 = plt.subplots()
ax3.bar(keys_list, values_list, alpha=0.8)
ax3.set_xlabel("year")
ax3.set_ylabel("count")
plt.xticks(rotation=-90, fontsize=10)  # تغییر اندازه نوشته‌های محور افقی
st.pyplot(fig3)


