import raven.collector
import raven.mqtt
import raven.watchdog
import logging
import time
import argparse
from configparser import RawConfigParser

kTopicMap = {
    ("InstantaneousDemand", "Demand"): "/energy/demand",
    ("CurrentSummationDelivered", "SummationDelivered"): "/energy/delivered",
    ("CurrentSummationDelivered", "SummationReceived"): "/energy/received",
}
kTopicName = { k[0] for k in kTopicMap.keys() }

kAsyncLoopTimeout = 5

kLog = logging.getLogger(__name__)


class Runner:
    def __init__(self, config_path):
        self.config = RawConfigParser()
        self.config.read(config_path)
        self.collector = raven.collector.Collector(
            config_path, read_callback=self.recv_message
        )
        self.mqtt = raven.mqtt.MosquittoClient(config_path)
        self.watchdog = raven.watchdog.Watchdog(
            self.config.getint("serial", "watchdog"), self._timeout
        )

    def start(self):
        self.mqtt.start()
        self.collector.start()
        self.watchdog.start()

    def stop(self):
        try:
            self.watchdog.stop()
        except RuntimeError:
            kLog.warning("Watchdog already stopped")
        self.collector.stop()
        self.mqtt.stop()

    def _timeout(self):
        kLog.warning("Watchdog timeout")
        self.stop()
        raise SystemExit("Watchdog timeout")

    def recv_message(self, message):
        self.watchdog.reset()
        if message.name not in kTopicName:
            logging.info(message)
            return
        if "TimeStamp" not in message:
            logging.error(message)
            return
        timestamp = message["TimeStamp"]
        for name, value in message.values():
            topic = kTopicMap[(message.name, name)]
            self.mqtt.publish(topic, timestamp, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Listens on the serial port for power usage information, and relays it to an MQTT server"
    )
    parser.add_argument("config", help="Path to configuration file")
    args = parser.parse_args()
    config = RawConfigParser()
    config.read(args.config)
    log_level = config.get("logging", "level")
    logging.basicConfig(level=getattr(logging, log_level))
    runner = Runner(args.config)
    runner.start()
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break
    runner.stop()
