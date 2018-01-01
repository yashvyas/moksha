# -*- coding: utf-8 -*-
from binance.client import Client as binance
from . import commands

class BinanceClient:
    COMMANDS = {'aggregate_trades': commands.AggregateTrades()}
    
    def __init__(self, key, secret):
        self.client = binance(key, secret)
    
    def help(self):
        for i in self.COMMANDS.values():
            i.help()
            
    def execute(self, cmd, symbol):
        if not cmd in self.COMMANDS:
            print "Command not implemented yet"
            print "available commands are.."
            self.help()
            return None
        
        command = self.COMMANDS[cmd]
        return command.execute(self.client, symbol)
        