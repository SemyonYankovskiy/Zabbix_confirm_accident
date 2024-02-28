from datetime import date

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from app.address_to_verbose import get_info_from_zabbix_node
from app.cache import cache
from app.has_outages import json_opener, has_outages
from app.rabbitmq import RabbitMQConnection
from app.zabbix import event_acknowledge


def message_callback(
    ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
) -> None:
    try:
        data: dict = orjson.loads(body)  # pylint: disable=maybe-no-member
        print("Got message", data)
    except orjson.JSONDecodeError:  # pylint: disable=maybe-no-member
        print("Invalid JSON")
        return

    event_id = data.get("EventID")
    host_name = data.get("HostName")

    street, house = get_info_from_zabbix_node(host_name)

    if not street and not house:
        return

    file_data = cache.get_or_cache(60 * 60, json_opener, f"data-{date.today()}.json")

    text_outages = has_outages((street, house), file_data)
    if text_outages:
        event_acknowledge(event_id, text_outages)


if __name__ == "__main__":
    connection = RabbitMQConnection()
    print("Connected to RabbitMQ")
    connection.start_consuming(callback=message_callback)
