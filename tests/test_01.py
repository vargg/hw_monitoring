import time
from datetime import datetime

from monitor.utils import DATE_FORMAT


class Test01API:
    def test_01_get_current_usage(self, client, fake_redis):
        with fake_redis:
            response = client.get('/api/usage/current/')

        response_data = response.json()

        assert response.status_code == 201, (
            '`/api/usage/current/`: некорректный код ответа'
        )

        assert response_data.get('date') is not None, (
            '`/api/usage/current/`: отсутствует поле `date` в '
            'возвращаемых данных'
        )

        assert response_data.get('cpu') is not None, (
            '`/api/usage/current/`: отсутствует поле `cpu` в '
            'возвращаемых данных'
        )

        assert response_data.get('memory') is not None, (
            '`/api/usage/current/`: отсутствует поле `memory` в '
            'возвращаемых данных'
        )

    def test_02_post_current_cpu_usage(self, client, fake_redis):
        data = ['cpu']
        with fake_redis:
            response = client.post(
                '/api/usage/current/',
                data=data,
                format='json',
            )

        response_data = response.json()

        assert response.status_code == 201, (
            '`/api/usage/current/`: некорректный код ответа'
        )

        assert response_data.get('date') is not None, (
            '`/api/usage/current/`: отсутствует поле `date` в '
            'возвращаемых данных'
        )

        assert response_data.get('cpu') is not None, (
            '`/api/usage/current/`: отсутствует поле `cpu` в '
            'возвращаемых данных'
        )

        assert response_data.get('memory') is None, (
            '`/api/usage/current/`: присутствует поле `memory` в '
            'возвращаемых данных'
        )

    def test_03_post_current_memory_usage(self, client, fake_redis):
        data = ['memory']
        with fake_redis:
            response = client.post(
                '/api/usage/current/',
                data=data,
                format='json',
            )

        response_data = response.json()

        assert response.status_code == 201, (
            '`/api/usage/current/`: некорректный код ответа'
        )

        assert response_data.get('date') is not None, (
            '`/api/usage/current/`: отсутствует поле `date` в '
            'возвращаемых данных'
        )

        assert response_data.get('cpu') is None, (
            '`/api/usage/current/`: присутствует поле `cpu` в '
            'возвращаемых данных'
        )

        assert response_data.get('memory') is not None, (
            '`/api/usage/current/`: отсутствует поле `memory` в '
            'возвращаемых данных'
        )

    def test_04_get_current_usage_list(self, client, fake_redis):
        with fake_redis:
            response = client.get('/api/usage/')
            len_before = len(response.json())

            n = 3
            for _ in range(n):
                # ключ - дата и время с точностью до секунды
                time.sleep(1)
                response = client.get('/api/usage/current/')

            response = client.get('/api/usage/')
            len_after = len(response.json())

        assert response.status_code == 200, (
            '`/api/usage/`: некорректный код ответа'
        )

        assert len_before + n == len_after, (
            '`/api/usage/`: не соответствует количество данных в ответе'
        )

    def test_05_post_current_usage(self, client, fake_redis):
        with fake_redis:

            n = 3
            for i in range(n):
                # ключ - дата и время с точностью до секунды
                time.sleep(1)
                if i == n - 1:
                    from_date = datetime.now().strftime(DATE_FORMAT)
                response = client.get('/api/usage/current/')
            until_date = datetime.now().strftime(DATE_FORMAT)

            data = {
                'from_date': from_date,
                'until_date': until_date
            }

            response = client.get('/api/usage/')
            len_before = len(response.json())

            response = client.post('/api/usage/', data=data, format='json')

            assert response.status_code == 204, (
                '`/api/usage/`: некорректный код ответа'
            )

            response = client.get('/api/usage/')
            len_middle = len(response.json())

            assert len_before == len_middle + 1, (
                '`/api/usage/`: не соответствует количество данных в ответе'
            )

            response = client.post('/api/usage/')

            assert response.status_code == 204, (
                '`/api/usage/`: некорректный код ответа'
            )

            response = client.get('/api/usage/')
            len_after = len(response.json())

            assert len_after == 0, (
                '`/api/usage/`: не соответствует количество данных в ответе'
            )
