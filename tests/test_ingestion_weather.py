import json
from unittest import TestCase
import shutil
from unittest.mock import patch

from src.ingestion import raw_ingestion_weather


class TestIngestionWeather(TestCase):
    def tearDown(self):
        shutil.rmtree("delta")

    @patch("src.ingestion.run_async_process")
    def test_ingestion_weather(self, mock_get):
        mock_get.return_value = json.load(open("test.json"))

