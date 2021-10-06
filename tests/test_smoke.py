import http
from src import app
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_smoke():
    client = app.test_client()
    resp = client.get('/smoke')
    assert resp.status_code == http.HTTPStatus.OK  # хранит код ответа 200
