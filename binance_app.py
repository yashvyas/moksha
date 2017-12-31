"""
@author shattang
"""

import yaml
import actor
from binance.client import Client
from binance.websockets import BinanceSocketManager

class BinanceApp(object):
    def __init__(self):
        self.config = {}

    def start(self, config_path=None, **kwargs):
        if config_path:
            with open(config_path, 'rb') as f:
                self.config = yaml.load(f)

        api_key = kwargs.get('api_key', self.config['api_key'])
        api_secret = kwargs.get('api_secret', self.config['api_secret'])
        self._client = Client(api_key, api_secret)
        self._socket_manager = BinanceSocketManager(self._client)
        num_executors = kwargs.get('num_executors', self.config.get('num_executors', 1))
        self.actor_system = actor.ActorSystem(num_executors)
        self._topic_storage = kwargs.get('topic_storage')
        if not self._topic_storage:
            from local_topic_storage import LocalTopicStorage
            storage_dir = kwargs.get('storage_dir', self.config['storage_dir'])
            self._topic_storage = LocalTopicStorage(storage_dir)

        self.rest_request_actor = actor.Actor(self._rest_request_actor_func)
        self.topic_storage_actor = actor.Actor(self._topic_storage_actor_func)
        self.run(**kwargs)

    def stop(self, timeout=None):
        self.actor_system.stop(timeout=timeout)

    def _topic_storage_actor_func(self, message):
        action = message['action']
        if action == 'store':
            topic = message['topic']
            data = message['data']
            key = message.get('key')
            self._topic_storage.store_topic_data(topic, data, key=key)
        elif action == 'get':
            topic = message['topic']
            key = message.get('key')
            recv_actor = message['from']
            result = self._topic_storage.get_topic_data(topic, key=key)
            res_msg = {'action': 'topic_get_result', 'request': message, 'result': result}
            self.actor_system.send_message(recv_actor, res_msg)

    def _rest_request_actor_func(self, message):
        req_func = message['func']
        recv_actor = message['from']
        try:
            result = req_func(self._client, message)
        except Exception as e:
            result = e
        res_msg = {'action': 'rest_result', 'request': message, 'result': result}
        self.actor_system.send_message(recv_actor, res_msg)

    def run(self, **kwargs):
        raise NotImplementedError()
