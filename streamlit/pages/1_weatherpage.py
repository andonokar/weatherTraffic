import streamlit as st
from config.loader import config
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, col

weather_path = f"{config['path']}/{config['weather']['folder_name']}_raw"
spark = SparkSession.builder.getOrCreate()
data = spark.read.format("delta").load(weather_path)
st.title("Weather Dashboard")

date_range = data.select(min(col("date")).alias("min"), max(col("date")).alias("max")).collect()[0]
city = st.selectbox("Select a city", config["cities"].keys(), None)
if city:
    lat, long = config["cities"][city]["lat"], config["cities"][city]["long"]
    city_df = data.where((data.lat == lat) & (data.long == long))
    range_data_min, range_data_max = st.date_input("Select date range", [date_range.min, date_range.max])
    pandas_data = city_df.where((city_df.date >= range_data_min) & (city_df.date <= range_data_max)).toPandas()
    st.subheader("Daily Data")
    st.subheader("Temperature Data")
    st.line_chart(pandas_data.set_index('date')[['min_temperature', 'max_temperature']])
    st.subheader("humidity data")
    st.line_chart(pandas_data.set_index('date')['humidity'])
    st.subheader("wind speed data")
    st.line_chart(pandas_data.set_index('date')['wind_speed'])
