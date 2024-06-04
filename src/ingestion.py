import asyncio
from typing import Coroutine
import aiohttp
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date
from pyspark.sql.types import *


async def fetch(session: aiohttp.ClientSession, url: str) -> Coroutine:
    """
    Function that calls the api for each url
    :param session: the ClientSession from aiohttp
    :param url: the endpoint of the url
    :return: a Coroutine containing the dict of the request output
    """
    async with session.get(url) as response:
        return await response.json()


async def fetch_all(urls: list[str]) -> tuple:
    """
    function that organizes every api call in async way
    :param urls: all urls that will be called
    :return: tuple of responses
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url))
        responses = await asyncio.gather(*tasks)
        return responses


def run_async_process(urls: list[str]) -> tuple:
    """
    Function that runs the async processing
    :param urls: all the urls that will be called
    :return: tuple of responses
    """
    responses = asyncio.run(fetch_all(urls))
    return responses


def raw_ingestion_weather(urls: list[str], spark: SparkSession, path: str) -> None:
    """
    Function that process the ingestion of the weather api
    :param urls: all the urls that will be called
    :param spark: the sparkSession
    :param path: where the files will be saved
    :return: None
    """
    responses = run_async_process(urls)

    responses = [{"coord": {x: float(y) for x, y in response.get("coord").items()},
                  "weather": response.get("weather"),
                  "main": response.get("main"),
                  "visibility": response.get("visibility"),
                  "clouds": response.get("clouds"),
                  "wind": {x: float(y) for x, y in response.get("wind").items()}} for response in responses if response["cod"] == 200]
    schema = (StructType()
              .add("coord", MapType(StringType(), DoubleType()))
              .add("weather", ArrayType(MapType(StringType(), StringType())))
              .add("main", StructType().add("temp_min", DoubleType()).add("temp_max", DoubleType()).add("humidity",
                                                                                                        LongType()))
              .add("visibility", LongType())
              .add("clouds", MapType(StringType(), LongType()))
              .add("wind", StructType().add("speed", DoubleType()))
              )
    df = spark.createDataFrame(responses, schema)
    final_df = df.select(
        col("coord").getField("lon").alias("lon"),
        col("coord").getField("lat").alias("lat"),
        col("weather").getItem(0).getField("description").alias("weather_description"),
        col("main").getField("temp_min").alias("min_temperature"),
        col("main").getField("temp_max").alias("max_temperature"),
        col("main").getField("humidity").alias("humidity"),
        col("visibility"),
        col("clouds").getField("all").alias("clouds"),
        col("wind").getField("speed").alias("wind_speed"),
        current_date().alias("date")
    )
    (final_df.write
     .mode("overwrite")
     .option("partitionOverwriteMode", "dynamic")
     .format("delta")
     .partitionBy("date")
     .save(path))
