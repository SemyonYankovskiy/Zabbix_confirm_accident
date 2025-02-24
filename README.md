## Запуск

### docker compose

Перед запуском нужно создать файл `.env` и указать в нём 
переменные окружения, которые обозначены в `env.sample`

    PROXY                   # URL для проксирования подключений к sevenergo и yandex картам

    EXTRA_HOST              # Для соответствия домена и IP адреса RabbitMQ в формате: domain:ip

    RABBITMQ_USER           # Пользователь RabbitMQ
    RABBITMQ_PASSWORD       # Пароль пользователя
    RABBITMQ_HOST           # Домен RabbitMQ
    RABBITMQ_PORT           # Порт 5671 для amqps
    RABBITMQ_VHOST          # Виртуальный хост, по умолчанию = /
    RABBITMQ_EXCHANGE       # Название exchange - zabbix-action
    RABBITMQ_QUEUE          # Название очереди - sevenergo
    RABBITMQ_ROUTING_KEY    # Название ключа маршрутизации - sevenergo
    
    ZABBIX_URL              # Должен быть формата https://localhost/zabbix
    ZABBIX_USER             # Пользователь, от коорого будут подписываться аварии
    ZABBIX_PASSWORD

### Сертификаты

Поместите файлы сертификатов для RabbitMQ сервера в папку `certs` рядом с 
файлом `docker-compose.yaml`

- `root.crt`: Корневой сертификат (cacert). В данном случае, этот файл представляет
    собой самоподписанный корневой сертификат, который используется для подписи клиентских сертификатов.
    Этот файл может быть распространен среди клиентов для проверки подлинности сервера.
- `client.key`: Закрытый ключ (private key) клиента. Этот ключ используется для создания 
    запроса на подпись сертификата клиента и для создания подписанного клиентского сертификата.
- `client.crt`: Подписанный клиентский сертификат. Этот файл содержит открытый ключ клиента, 
    данные о клиенте и подпись, сгенерированную закрытым ключом сервера (root key).

Подробнее про создание данных сертификатов можно почитать [здесь](https://github.com/ig-rudenko/rabbitmq-notifier).


## Разработка

Установите дополнительные зависимости необходимые для разработки

### Тестирование

```shell
pip install -r requirements-dev.txt
```

```shell
python -m unittest discover tests -v
```

#### Проверка типизации

```shell
mypy app geo_map
```
#### Линтер

```shell
pylint app geo_map
```

### Запуск парсера и GeoMap

Необходимо указать переменные окружения, для отправки файла `geojson` 
на определённый слой в программе `ecstasy`:

    ECSTASY_API_URL       # http://domain
    ECSTASY_API_USERNAME
    ECSTASY_API_PASSWORD
    ECSTASY_LAYER_NAME    # название слоя

```shell
python main-parser.py
```

### Запуск обработчика событий

Необходимо указать переменные окружения:

    RABBITMQ_USER
    RABBITMQ_PASSWORD
    RABBITMQ_HOST
    RABBITMQ_PORT
    RABBITMQ_VHOST
    RABBITMQ_CACERT
    RABBITMQ_CERTFILE
    RABBITMQ_KEYFILE
    RABBITMQ_EXCHANGE=zabbix-action
    RABBITMQ_QUEUE=sevenergo
    RABBITMQ_ROUTING_KEY=sevenergo

    ZABBIX_URL
    ZABBIX_USER
    ZABBIX_PASSWORD

Команда запуска:

```shell
python consumer.py
```