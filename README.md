# HW_monitor.

http://178.154.228.102/

## Стэк
[Python](https://www.python.org/) v.3.9, [Django](https://www.djangoproject.com/) v.3.2.8, [Django REST framework](https://www.django-rest-framework.org/) v.3.12.4, [Redis](https://redis.io/documentation) v.6.2, [Docker](https://www.docker.com/) v.20.10.8.

## Описание.
Web-сервис, позволяющий узнать текущую загрузку сервера: ЦПУ, ОЗУ, ГПУ (при наличии; поддерживаются только ГПУ от NVIDIA); каждый запрос сохраняется, можно получить все запросы в формате "время запроса MM:DD:hh:mm:ss": {"метод запроса", **"запрошенные данные"}.

## API.
Доступ к сервису осуществляется через API.

### Пример запроса:
- получение всех значений загрузки

request `api/usage/current/ [GET]`

response
```
{
  "date": "str",  # дата в формате MM:DD:hh:mm:ss
  "cpu": float,  # загрузка ЦПУ в процентах
  "gpu": float,  # загрузка ГПУ в процентах
  "memory": float  # загрузка ОЗУ в процентах
}
```

- получение отдельных значений загрузки

request `api/usage/current/ [POST]`
```
["cpu", "memory"]
```
response
```
{
  "date": "str",
  "cpu": float,
  "memory": float
}
```

- получение информации по обработанным запросам

request `api/usage/ [GET]`

response
```
{
  "date": "str",
  "cpu": float,
  "gpu": float,
  "memory": float,
  "request_method": "str"  # метод запроса
}
{
  ...
}
...
```

- удаление всей информации по обработанным запросам

request `api/usage/ [POST]`

## Установка и запуск.
Для запуска требуются [docker](https://docs.docker.com/get-docker/) и [docker compose](https://docs.docker.com/compose/install/).
Клонировать репозиторий:
```shell
git clone https://github.com/vargg/yamdb_final.git
```
В корневом каталоге проекта создать файл `.env` в котором должны быть заданы следующие переменные:
```
-DJANGO_SECRET_KEY
```
Проект может быть запущен без явного указания `DJANGO_SECRET_KEY` в файле `.env`. В данном случае будет использовано случайное значение `SECRET_KEY` (функция get_random_secret_key).

Запуск контейнеров:
```shell
docker-compose up
```
Сервис будет доступен по ссылке [http://localhost](http://localhost).

Остановка:
```shell
docker-compose down
```
