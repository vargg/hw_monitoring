import pytest
from django.core.cache.backends.locmem import LocMemCache
from django.test import override_settings
from django_fakeredis import FakeRedis


class UpgradeLocMemCache(LocMemCache):

    def set(self, key, value):
        self._cache[key] = value

    def get(self, key):
        return self._cache[key]

    def delete(self, key):
        self._cache.pop(key)

    def keys(self, key):
        return self._cache.keys()


@pytest.fixture
def client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def fake_redis():
    fake_redis = FakeRedis("monitor.views.cache")
    fake_redis.override_settings = override_settings(
            CACHES={
                "default": {
                    "BACKEND": 'tests.fixtures.fixture.UpgradeLocMemCache'
                }
            }
        )
    return fake_redis
