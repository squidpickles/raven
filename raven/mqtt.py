import json
import logging
from configparser import RawConfigParser

import paho.mqtt.client as mqtt

kLog = logging.getLogger(__name__)


class MosquittoClient:
    def __init__(self, config_path):
        config = RawConfigParser()
        config.read(config_path)
        protocol = mqtt.MQTTv31
        if config.has_option("mqtt", "use311") and config.getboolean("mqtt", "use311"):
            kLog.debug("311")
            protocol = mqtt.MQTTv311
        self.name = config.get("mqtt", "client_name")
        client = mqtt.Client(client_id=self.name, clean_session=True, protocol=protocol)
        client.username_pw_set(config.get("mqtt", "username"), config.get("mqtt", "password"))
        client.tls_set(config.get("mqtt", "ca_cert"))
        if config.get("mqtt", "hostname") in ("localhost", "127.0.0.1", "::1"):
            client.tls_insecure_set(True)
        self.config = config
        self.client = client

    def start(self):
        hostname = self.config.get("mqtt", "hostname")
        port = int(self.config.get("mqtt", "port"))
        kLog.debug("Connecting to MQTT server at %s:%s", hostname, port)
        self.client.connect(hostname, port)
        self.client.loop_start()
        kLog.info("Connected to MQTT server")

    def stop(self):
        kLog.debug("Disconnecting from MQTT server")
        self.client.disconnect()
        self.client.loop_stop()
        kLog.info("Disconnected from MQTT server")

    def publish(self, topic, timestamp, value):
        payload = json.dumps({"ts": timestamp, "val": value})
        topic = self.name + topic
        kLog.debug("Publishing %s to %s", payload, topic)
        self.client.publish(topic, payload, qos=1)
