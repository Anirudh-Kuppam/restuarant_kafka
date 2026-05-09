from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

items = ["Burger","Pizza","Pasta","Coffee"]

while True:
    order = {
        "item": random.choice(items),
        "price": random.randint(50,300),
        "quantity": random.randint(1,3)
    }
    producer.send('orders', order)
    print(order)
    time.sleep(2)