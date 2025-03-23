import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_get_data(self):
        response = client.get("/data")
        self.assertEqual(response.status_code, 200)

    def test_post_data(self):
        sample_data = {
            "datetime": "2025-03-23T10:00:00",
            "open": 100.5,
            "high": 105.0,
            "low": 99.5,
            "close": 102.5,
            "volume": 1500
        }
        response = client.post("/data", json=sample_data)
        self.assertEqual(response.status_code, 200)

    def test_strategy_performance(self):
        response = client.get("/strategy/performance")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
