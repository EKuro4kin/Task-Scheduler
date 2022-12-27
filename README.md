# Gриложение "Календарь"
Предоставляет возможности для работы со встречами, а так же с целями и даёт возможность отслеживать прогресс по ним.

## стек (python3.10, Django 4.0.1, PostgreSQL)


### Перед началом работы:

#### Установка зависимостей:

В корневой папке находиться файл с зависимостями requirements.txt
```shell
pip install -r requirements.txt
```

#### Развертывание базы данных:

Для удобства развертывания базы данных в папке postgresql находиться файл docker-compose 

````shell
cd /postgresql
docker-compose up -d 
````

#### Настройка переменных окружения:

Для работы проекта необходимо создать **.env** в корневой папке.
В нем нужно указать необходимые значения переменных:

* DEBUG=True (или False) - **включения или выключения дебагера django**
* SECRET_KEY = **секретный ключ**
* DATABASE_URL = **psql://<имя пользователя>:<пароль пользователя>@<ip адрес>:<порт>/<имя базы>**
* SOCIAL_AUTH_VK_OAUTH2_KEY = **ключ приложения ВК**
* SOCIAL_AUTH_VK_OAUTH2_SECRET = **секрет приложения ВК**
* TG_BOT_API_TOKEN = **токен телеграм бота**


### Запуск проекта Django:

* Перед запуском проекта, накатываем миграции на базу данных командой

```shell
python ./manage.py migrate
```
* Запуск проекта

```shell
python ./manage.py runserver
```

### Запуск телеграм бота:

* Команда для запуска телеграм бота

````shell
python ./manage.py runbot
````