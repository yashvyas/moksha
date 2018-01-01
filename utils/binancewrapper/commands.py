# -*- coding: utf-8 -*-

# Interface
class Command:
    def execute(self, client, tickr):
        raise NotImplementedError()
        
    def name(self):
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()
        
    def help(self):
        print "{}: {}".format(self.name(), self.description())
    
    
        
class AggregateTrades(Command):
    
    def execute(self, client, tickr):
        return client.get_aggregate_trades(symbol=tickr)
    
    def name(self):
        return "aggregate_trades"
#        return self.name
    
    def description(self):
        return "get aggregate trades on binance given a tickr symbol"

