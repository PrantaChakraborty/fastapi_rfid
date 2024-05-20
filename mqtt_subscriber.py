"""
mqtt subscriber
"""
import json
import logging
from json import JSONDecodeError

import paho.mqtt.client as mqtt

from exceptions import MqttException

logger = logging.getLogger(__name__)


def process_message(message: dict) -> None:
    pass


def on_message(cl, userdata, message):
    """
    receive message from mqtt broker
    """
    try:
        content = str(message.payload.decode("utf-8"))
        json_message = json.loads(content)
        process_message(json_message)
    except JSONDecodeError as json_error:
        logger.error("message is: %s", json_error)
    except MqttException as e:
        logger.exception(e)


# initialize the broker
# for test purpose
MQTT_BROKER = "mqtt.eclipseprojects.io"
client = mqtt.Client()
client.connect(MQTT_BROKER, port=1883)

# for production

# MQTT_BROKER = setup.os.environ.get('MQTT_BROKER')
# client = mqtt.Client()
# client.username_pw_set(username=setup.os.environ.get('MQTT_USERNAME'),
#                        password=setup.os.environ.get('MQTT_PASSWORD'))
# client.connect(MQTT_BROKER, port=int(os.environ.get('MQTT_PORT')))

if __name__ == '__main__':
    # subscribe to the topic topic_list = ['zicore/hardware/hub-1',
    #  'zicore/hardware/hub-2', 'zicore/hardware/hub-3',
    # 'zicore/hardware/hub-4', 'zicore/hardware/hub-5']

    # will subscribe similar like topic list
    client.subscribe('mahfuj/hardware/')
    client.on_message = on_message
    print('server started')
    client.loop_forever()
