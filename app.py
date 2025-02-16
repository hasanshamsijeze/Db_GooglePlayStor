import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# دریافت داده‌ها از API
def fetch_apps():
    response = requests.get(f"{API_URL}/apps/")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

# اضافه کردن اپلیکیشن جدید
def add_app(app_data):
    response = requests.post(f"{API_URL}/apps/", json=app_data)
    return response.json()

# به‌روزرسانی اپلیکیشن
def update_app(app_id, app_data):
    response = requests.put(f"{API_URL}/apps/{app_id}", json=app_data)
    return response.json()

# حذف اپلیکیشن
def delete_app(app_id):
    response = requests.delete(f"{API_URL}/apps/{app_id}")
    return response.json()

# طراحی داشبورد
def app():
    st.title("📊 Google Play Store Dashboard")

    # **۱. نمایش لیست اپلیکیشن‌ها**
    st.subheader("📋 لیست اپلیکیشن‌ها")
    apps_df = fetch_apps()
    st.dataframe(apps_df)

    # **۲. اضافه کردن اپلیکیشن جدید**
    st.subheader("➕ اضافه کردن اپلیکیشن جدید")
    with st.form("add_app_form"):
        app_id = st.text_input("🆔 App ID")
        app_name = st.text_input("📱 نام اپلیکیشن")
        category_id = st.number_input("📂 دسته‌بندی (Category ID)", min_value=1, step=1)
        rating = st.slider("⭐ امتیاز", 0.0, 5.0, 3.0, 0.1)
        installs = st.number_input("📥 تعداد نصب", min_value=0, step=1000)
        submit_button = st.form_submit_button("افزودن اپلیکیشن")

        if submit_button:
            new_app = {
                "app_id": app_id,
                "app_name": app_name,
                "category_id": category_id,
                "rating": rating,
                "rating_count": 0,
                "installs": installs,
                "min_installs": installs,
                "max_installs": installs,
                "free": True,
                "price": 0.0,
                "currency": "USD",
                "size": "Varies",
                "min_android": "4.0",
                "developer_id": 1,
                "released": "2024-01-01",
                "last_updated": "2024-01-01",
                "content_rating": "Everyone",
                "privacy_policy": "None",
                "ad_supported": False,
                "in_app_purchases": False,
                "editors_choice": False
            }
            response = add_app(new_app)
            st.success(response["message"])

    # **۳. ویرایش اپلیکیشن**
    st.subheader("✏ ویرایش اپلیکیشن")
    app_to_edit = st.selectbox("انتخاب اپلیکیشن برای ویرایش", apps_df["app_name"] if not apps_df.empty else [])
    if app_to_edit:
        selected_app = apps_df[apps_df["app_name"] == app_to_edit].iloc[0]
        with st.form("edit_app_form"):
            new_rating = st.slider("⭐ امتیاز جدید", 0.0, 5.0, float(selected_app["rating"]), 0.1)
            update_button = st.form_submit_button("بروزرسانی اپلیکیشن")

            if update_button:
                updated_data = selected_app.to_dict()
                updated_data["rating"] = new_rating
                response = update_app(selected_app["app_id"], updated_data)
                st.success(response["message"])

    # **۴. حذف اپلیکیشن**
    st.subheader("🗑 حذف اپلیکیشن")
    app_to_delete = st.selectbox("انتخاب اپلیکیشن برای حذف", apps_df["app_name"] if not apps_df.empty else [])
    if app_to_delete:
        selected_app = apps_df[apps_df["app_name"] == app_to_delete].iloc[0]
        delete_button = st.button("❌ حذف اپلیکیشن")

        if delete_button:
            response = delete_app(selected_app["app_id"])
            st.success(response["message"])

if __name__ == "__main__":
    app()
