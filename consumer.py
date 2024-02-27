from app.rabbitmq import RabbitMQConnection


def main():
    connection = RabbitMQConnection()
    print("Connected to RabbitMQ")
    print("Starting consumer...")
    connection.start_consuming()


if __name__ == "__main__":
    main()
