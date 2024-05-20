"""
mqtt subscriber
"""
import json
import logging
from json import JSONDecodeError

import paho.mqtt.client as mqtt

from exceptions import MqttException

from src.rfid.service import create_rfid

from config import setting

logger = logging.getLogger(__name__)


def process_message(message: json) -> None:
    create_rfid(message)
    return None


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


MQTT_BROKER = setting.mqtt_host
client = mqtt.Client()
client.username_pw_set(username=setting.mqtt_username,
                       password=setting.mqtt_password)
client.connect(MQTT_BROKER, port=setting.mqtt_port)

if __name__ == '__main__':

    # will subscribe similar like topic list
    client.subscribe('mahfuj/hardware/thesis')
    client.on_message = on_message
    print('server started')
    client.loop_forever()
