from kombu import Connection, Exchange, Queue
from lisa_api.lisa.configuration import CONF as config
import logging
logger = logging.getLogger('lisa_api')


def send_message(message, zone='all', source='api'):
    if not zone:
        zone = 'all'
    lisa_exchange = Exchange('lisa', 'topic', durable=True)
    client_queue = Queue('client', exchange=lisa_exchange, routing_key='client.all')

    rabbitmq_creds = {
        'user': config.rabbitmq.user,
        'password': config.rabbitmq.password,
        'host': config.rabbitmq.host,
    }

    with Connection('amqp://{user}:{password}@{host}//'.format(**rabbitmq_creds),
                    transport_options={'confirm_publish': True}) as conn:
        producer = conn.Producer(serializer='json')
        producer.publish({'message': message, 'zone': zone, 'source': source},
                         exchange=lisa_exchange, routing_key='client.%s' % zone,
                         declare=[client_queue])
        logger.debug(msg='Publishing a message on %s, with %s' %
                         ('client.' + zone,
                          {'message': message, 'zone': zone, 'source': source}))
