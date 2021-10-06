import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from src import app
import http
import json
from unittest.mock import patch
from dataclasses import dataclass

@dataclass
class FakeFilm:
    title = 'Fake Film'
    distributed_by = 'Fake'
    release_date = '2002-12-03'
    description = 'Fake description'
    length = 100
    rating = 8.0

class TestFilms:
    uuid = []
    def test_get_films_with_db(self):
        client= app.test_client()
        resp=client.get('/films')

        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.services.film_service.FilmService.fetch_all_films', autospec= True)
    def test_get_films_mock_db(self, mock_db_call): #mock_db_call можно назвать как хочу
        client = app.test_client()
        resp = client.get('/films')
        mock_db_call.assert_called_once() # проверка, был ли вызван наш мок один раз
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_film_with_db(self):
        client = app.test_client()
        data = {
            'title': 'Test Title',
            'distributed_by': 'Test Company',
            'release_date': '2010-10-01',
            'description': '',
            'length': 100,
            'rating': 8.0
        }
        resp=client.post('/films', data = json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['title'] == 'Test Title'
        self.uuid.append(resp.json['uuid']) # получаем uuid, чтобы удалить из бд после теста

    def test_create_film_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit: # мокаем методы add и commit
            client = app.test_client()
            data = {
                'title': 'Test Title',
                'distributed_by': 'Test Company',
                'release_date': '2010-04-01',
                'description': '',
                'length': 100,
                'rating': 8.0
            }
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
    
    def test_update_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        data = {
            'title': 'Update Title',
            'distributed_by': 'update',
            'release_date': '2010-04-01'
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['title'] == 'Update Title'

    def test_update_film_with_mock_db(self):
        with patch('src.services.film_service.FilmService.fetch_film_by_uuid') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeFilm() # создаем фейковый фильм, который апдейтим
            client = app.test_client()
            url = f'/films/1'
            data = {
                'title': 'Update Title',
                'distributed_by': 'update',
                'release_date': '2010-04-01'
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT