import json
from unittest import TestCase
import shutil
from unittest.mock import patch
from pyspark.sql import SparkSession
from src.ingestion import raw_ingestion_weather


class TestIngestionWeather(TestCase):
    def setUp(self):
        self.spark = SparkSession.builder.getOrCreate()

    def tearDown(self):
        shutil.rmtree("delta")

    @patch("src.ingestion.run_async_process")
    def test_ingestion_weather(self, mock_get):
        with open("test.json") as file:
            mock_get.return_value = json.load(file)
        raw_ingestion_weather(["test"], self.spark, "delta")
        df = self.spark.read.format("delta").load("delta")
        self.assertEqual(10, df.count())

