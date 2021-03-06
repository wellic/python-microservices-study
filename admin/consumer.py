import json
import os

import django
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product
from settings import RABBITMQ_URL

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    try:
        id = json.loads(body)
        print(id)
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        product.save()
        print('Product likes increase')
    except:
        pass


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
