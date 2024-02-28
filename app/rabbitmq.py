import ssl

import pika
from pika import exceptions

from app.misc import get_environ


class RabbitMQConnection:  # pylint: disable=too-few-public-methods
    class _Config:
        user: str = get_environ("RABBITMQ_USER")
        password: str = get_environ("RABBITMQ_PASSWORD")
        host: str = get_environ("RABBITMQ_HOST")
        port: str = get_environ("RABBITMQ_PORT")
        vhost: str = get_environ("RABBITMQ_VHOST")
        cacert: str = get_environ("RABBITMQ_CACERT")
        certfile: str = get_environ("RABBITMQ_CERTFILE")
        keyfile: str = get_environ("RABBITMQ_KEYFILE")
        exchange: str = get_environ("RABBITMQ_EXCHANGE")
        queue_name: str = get_environ("RABBITMQ_QUEUE")
        routing_key: str = get_environ("RABBITMQ_ROUTING_KEY")

    def __init__(self):
        context = ssl.create_default_context(cafile=self._Config.cacert)
        context.load_cert_chain(self._Config.certfile, self._Config.keyfile)
        ssl_options = pika.SSLOptions(context, self._Config.host)

        self._rmq_url_connection_str = pika.ConnectionParameters(
            host=self._Config.host,
            port=self._Config.port,
            virtual_host=self._Config.vhost,
            ssl_options=ssl_options,
            credentials=pika.credentials.PlainCredentials(
                username=self._Config.user, password=self._Config.password
            ),
        )

    def start_consuming(self, callback):
        while True:
            print("Starting consumer...")
            connection = pika.BlockingConnection(self._rmq_url_connection_str)
            try:
                with connection.channel() as channel:
                    if channel is not None:
                        channel.exchange_declare(
                            exchange=self._Config.exchange, exchange_type="direct", durable=True
                        )
                        channel.queue_declare(queue=self._Config.queue_name, durable=True)
                        channel.queue_bind(
                            exchange=self._Config.exchange,
                            queue=self._Config.queue_name,
                            routing_key=self._Config.routing_key,
                        )
                        channel.basic_consume(
                            queue=self._Config.queue_name,
                            on_message_callback=callback,
                            auto_ack=True,
                        )
                        channel.start_consuming()

            # Don't recover if connection was closed by broker
            except exceptions.ConnectionClosedByBroker as exc:
                print("exceptions.ConnectionClosedByBroker", exc)
                break
            # Don't recover on channel errors
            except exceptions.AMQPChannelError as exc:
                print("exceptions.AMQPChannelError", exc)
                break
            # Recover on all other connection errors
            except exceptions.AMQPConnectionError as exc:
                print("exceptions.AMQPConnectionError", exc)

            except KeyboardInterrupt:
                print("Connection closed by user")
                break
