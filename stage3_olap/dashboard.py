import streamlit as st
import pandas as pd
import plotly.express as px
import ydb

st.set_page_config(page_title="Мониторинг YDB", layout="wide")
st.title("📊 Аналитика городской инфраструктуры (YDB)")

@st.cache_data(ttl=60)
def load_data():
    endpoint = "grpc://localhost:2136"
    database = "/local"

    with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
        driver.wait(timeout=5, fail_fast=True)
        with ydb.QuerySessionPool(driver) as pool:
            result = pool.execute_with_retries("""
                SELECT timestamp, temperature, humidity
		FROM sensor_readings_column
		WHERE sensor_id = 1
		ORDER BY timestamp
		LIMIT 5000
            """)
            rows = result[0].rows
            return pd.DataFrame(rows)

with st.spinner('Загрузка данных из YDB...'):
    df = load_data()

if not df.empty:
    st.success(f"Успешно загружено {len(df)} записей для датчика №42.")

    fig_temp = px.line(df, x='timestamp', y='temperature', 
                       title='Температура за последние 30 дней',
                       labels={'timestamp': 'Время', 'temperature': 'Температура (°C)'})
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_hum = px.line(df, x='timestamp', y='humidity', 
                      title='Влажность за последние 30 дней',
                      labels={'timestamp': 'Время', 'humidity': 'Влажность (%)'})
    st.plotly_chart(fig_hum, use_container_width=True)
else:
    st.warning("Данные для датчика №42 за последние 30 дней не найдены. Проверьте, что данные загружены в колоночную таблицу.")
