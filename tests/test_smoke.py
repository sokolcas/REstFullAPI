import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from src import app
import http

def test_smoke():
    client = app.test_client()
    resp = client.get('/smoke')
    assert resp.status_code == http.HTTPStatus.OK # хранит код ответа 200
