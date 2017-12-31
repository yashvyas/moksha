"""
@author shattang
"""

from binance_app import BinanceApp
from collections import OrderedDict
from actor import Actor

class BinanceSymbolTradeRepo(Actor):
    def __init__(self, symbol, app):
        super(BinanceSymbolTradeRepo, self).__init__(self)
        self.symbol = symbol
        self.app = app #type: BinanceApp
        self._topic = ".".join(["binance.trades", symbol])

    def __call__(self, *args, **kwargs):
        message = args[0]
        action = message['action']
        if action == 'init':
            self._init()
        elif action == 'topic_get_result':
            self._on_topic_get_result(message)

    def _on_topic_get_result(self, message):
        pass

    def _init(self):
        actor = self.app.topic_storage_actor
        msg = {'action': 'get', 'topic': self._topic, 'from': self}
        self.app.actor_system.send_message(actor, msg)

class BinanceTradeRepo(Actor):
    def __init__(self, symbol_list, app):
        super(BinanceTradeRepo, self).__init__(self)
        self.app = app #type: BinanceApp
        self._symbol_repos = {}
        for symbol in symbol_list:
            self._add_symbol(symbol)

    def _add_symbol(self, symbol):
        sym = symbol.upper()
        if not sym in self._symbol_repos:
            actor = Actor(BinanceSymbolTradeRepo(sym, self.app))
            self._symbol_repos[sym] = actor
            self.app.actor_system.send_message(actor, {'action': 'init'})

    def __call__(self, message):
        action = message['action']
        if action == 'add_symbol':
            self._add_symbol(message['symbol'])
