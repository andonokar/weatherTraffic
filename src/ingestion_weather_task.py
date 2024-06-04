from src.loader import config
from src.ingestion import raw_ingestion_weather
from datetime import date

from pyspark.sql import SparkSession
builder = SparkSession.builder
spark = builder.getOrCreate()
city_info = config["cities"]
urls = [config["weather"]["endpoint"].format(lat=city["lat"], lon=city["long"], key=config["weather"]["api_key"])
        for city in config["cities"].values()]
weather_path = f"{config['path']}/{config['weather']['folder_name']}_raw"
raw_ingestion_weather(urls, spark, weather_path)
